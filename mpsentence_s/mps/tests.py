from django.utils.http import urlencode

from django.test import TestCase

# Create your tests here.
import datetime

from django.test import TestCase
from django.utils import timezone

from .models import User, Sentence
from django.urls import reverse

"""use following command to test

(venv) bash-3.2$ python manage.py test mps

"""


def build_url_with_params(view_path, params):
    url = reverse(view_path)
    url += '?' + urlencode(params)
    return url


def create_save_user(id=0, openId="test_openid", code="test_code", sessionKey="test_sessionkey",
                    unionId="", avatarUrl="test_avatarUrl",
                    city="test_city", country="test_country", gender=0, language="Zh",
                    nickName="test_nickName", province="test_province", email="test_email",
                    createTime=timezone.now()):

    user = User(id, openId, code, sessionKey,
                unionId, avatarUrl,
                city, country, gender, language,
                nickName, province, email,
                createTime)
    user.save()
    return user


def create_save_sentence(id, user, date, content, createTime=timezone.now()):
    sentence = Sentence(id, user.id, date, content, createTime)
    sentence.save()
    return sentence


class UserModelTests(TestCase):
    def test_user_create(self):
        user = create_save_user(id=0, openId="test_openid")
        self.assertEqual(user.openId, "test_openid")

    def test_sentence_create(self):
        user = create_save_user(id=0, openId="test_openid")
        sentence = create_save_sentence(id=0, user=user, date=timezone.now(), content="test_sentence")
        self.assertEqual(sentence.content, "test_sentence")


class SentenceApiTests(TestCase):
    def test_sentence_get(self):
        user = create_save_user(id=0, openId="test_openid")
        sentence = create_save_sentence(id=0, user=user, date=timezone.now(), content="test_sentence")
        date = str(timezone.now().date())
        # url = "%s?date=%s" % (reverse('sentence'), date)
        url = build_url_with_params('sentence', {'date': date})
        response = self.client.get(url)
        res = dict()
        res['sentenceId'] = 0
        res['sentence'] = "test_sentence"
        res['nickName'] = "test_nickName"
        res['avatarUrl'] = "test_avatarUrl"
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(
            str(response.content, encoding='utf8'),
            {'error_code': 0, 'msg': 'get sentence ok', 'data': res}
        )

