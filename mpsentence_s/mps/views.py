import datetime
import json
import requests

from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone

# Create your views here.

from .models import User, Sentence, Translate, Comment


def index(request):
    return HttpResponse("Hello, world. You're at the mps index.")


@csrf_exempt
def daily_sentence(request, date_id):
    content = "Today is a good day."
    usr = "default user"
    if request.method == 'POST':
        response = JsonResponse({'date': date_id, 'sentence': content, 'usr': usr}, safe=False)
    else:
        response = JsonResponse({'date': date_id+1, 'sentence': content, 'usr': usr}, safe=False)

    return response


@csrf_exempt
def get_openid(request):
    if request.method == 'GET':
        appId = request.GET.get('appId')
        code = request.GET.get('code')
        secret = request.GET.get('secret')
        if appId and code and secret:
            wechat_code2session_url = """https://api.weixin.qq.com/sns/jscode2session?appid={APPID}&secret={SECRET}&js_code={JSCODE}&grant_type=authorization_code
""".format(APPID=appId, SECRET=secret, JSCODE=code)
            response = json.loads(requests.get(wechat_code2session_url).content)  # 将json数据包转成字典
            if 'errcode' in response:
                return JsonResponse({'code': response['errcode'], 'msg': response['errmsg'], 'data': ''})
            openId = response['openid']
            sessionKey = response['session_key']
            user, created = User.objects.get_or_create(openId=openId)
            user.sessionKey = sessionKey
            user.code = code
            user.save()
            data = {'openid': openId, 'session_key': sessionKey}
            return JsonResponse({'error_code': 0, 'msg': 'get openId success', 'data': data})
        fail_msg = 'fail! No enough params:appId={} code={} secret={} to fetch openId'.format(appId, code, secret)
        return JsonResponse({'error_code': -1, 'msg': fail_msg, 'data': ''})


@csrf_exempt
def user_register(request):
    if request.method == 'POST':
        body = request.body
        params = json.loads(body)
        openId = params.get('openId')
        avatarUrl = params.get('avatarUrl', '')
        city = params.get('city', '')
        country = params.get('country', '')
        gender = params.get('gender', 0)
        language = params.get('language', '')
        nickName = params.get('nickName', '')
        province = params.get('province', '')
        if openId:
            user, created = User.objects.get_or_create(openId=openId)
            user.avatarUrl = avatarUrl
            user.city = city
            user.country = country
            user.gender = gender
            user.city = city
            user.language = language
            user.nickName = nickName
            user.province = province
            user.save()
            return JsonResponse({'error_code': 0, 'msg': 'register ok', 'data': ''})
        fail_msg = 'user register fail! no openId param'
        return JsonResponse({'error_code': -1, 'msg': fail_msg, 'data': ''})


@csrf_exempt
def sentence(request):
    if request.method == 'POST':
        body = request.body
        params = json.loads(body)
        openId = params.get('openId')
        sentence = params.get('sentence', '')
        date = timezone.now().date()
        if openId:
            user = User.objects.filter(openId=openId)[0]
            s, created = Sentence.objects.get_or_create(date=date)
            s.user = user
            s.content = sentence
            s.date = date
            s.save()
            return JsonResponse({'error_code': 0, 'msg': 'submit sentence ok', 'data': ''})
        fail_msg = 'submit sentence fail! no openId param'
        return JsonResponse({'error_code': -1, 'msg': fail_msg, 'data': ''})


@csrf_exempt
def translate(request):
    if request.method == 'POST':
        body = request.body
        params = json.loads(body)
        openId = params.get('openId')
        translate = params.get('translate', '')
        date = timezone.now().date()
        if openId:
            user = User.objects.filter(openId=openId)[0]
            s = Sentence.objects.filter(date=date).first()
            t = Translate(user=user, content=translate, sentence=s)
            t.save()
            return JsonResponse({'error_code': 0, 'msg': 'submit translate ok', 'data': ''})
        fail_msg = 'submit translate fail! no openId param'
        return JsonResponse({'error_code': -1, 'msg': fail_msg, 'data': ''})
    elif request.method == 'GET':
        date_string = request.GET.get('date')
        if date_string:
            y, m, d = date_string.split('/')
            # client should send UTC date to server, because server use UTC time when create records in database.
            date = datetime.datetime(int(y), int(m), int(d))
            s = Sentence.objects.filter(date=date).first()
            if not s:
                return JsonResponse({'error_code': 0, 'msg': 'no sentence today! get translates ok', 'data': ''})

            translates = Translate.objects.filter(sentence=s).order_by('-createTime')
            trans_list = list()
            for item in translates:
                res = dict()
                res['translateId'] = item.id
                res['sentence'] = item.sentence.content
                res['nickName'] = item.user.nickName
                res['avatarUrl'] = item.user.avatarUrl
                res['content'] = item.content
                res['numberOfLikes'] = item.numberOfLikes
                res['numberOfComments'] = item.numberOfComments
                trans_list.append(res)
            res_data = {'sentence': s.content, 'translates': trans_list}
            return JsonResponse({'error_code': 0, 'msg': 'get translates ok', 'data': res_data})
        fail_msg = 'get translates fail! no date param'
        return JsonResponse({'error_code': -1, 'msg': fail_msg, 'data': ''})


@csrf_exempt
def translate_update(request):
    if request.method == 'POST':
        body = request.body
        params = json.loads(body)
        translateId = params.get('translateId', None)
        numberOfLikes = params.get('numberOfLikes', None)
        numberOfComments = params.get('numberOfComments', None)
        if translateId is not None:
            translate = Translate.objects.filter(id=translateId).first()
            if translate:
                if numberOfLikes is not None:
                    translate.numberOfLikes = numberOfLikes
                if numberOfComments is not None:
                    translate.numberOfComments = numberOfComments
                translate.save()
            return JsonResponse({'error_code': 0, 'msg': 'update translate ok', 'data': ''})
        fail_msg = 'update translate fail! no translateId param'
        return JsonResponse({'error_code': -1, 'msg': fail_msg, 'data': ''})


@csrf_exempt
def comment(request):
    if request.method == 'POST':
        body = request.body
        params = json.loads(body)
        openId = params.get('openId')
        translateId = params.get('translateId')
        comment = params.get('comment', '')
        if openId and translateId:
            user = User.objects.filter(openId=openId)[0]
            t = Translate.objects.filter(id=translateId)[0]
            c = Comment(user=user, translate=t, content=comment)
            c.save()
            t.numberOfComments += 1
            t.save()
            return JsonResponse({'error_code': 0, 'msg': 'submit comment ok', 'data': ''})
        fail_msg = 'submit comment fail! no openId or translateId param'
        return JsonResponse({'error_code': -1, 'msg': fail_msg, 'data': ''})
    elif request.method == 'GET':
        translateId = request.GET.get('translateId')
        if translateId:
            comments = Comment.objects.filter(translate_id=translateId).order_by('-createTime')
            comments_list = list()
            for item in comments:
                res = dict()
                res['commentId'] = item.id
                res['nickName'] = item.user.nickName
                res['avatarUrl'] = item.user.avatarUrl
                res['content'] = item.content
                comments_list.append(res)
            return JsonResponse({'error_code': 0, 'msg': 'get translates ok', 'data': comments_list})
        fail_msg = 'get comments fail! no translateId param'
        return JsonResponse({'error_code': -1, 'msg': fail_msg, 'data': ''})
