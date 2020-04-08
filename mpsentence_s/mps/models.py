import datetime
from django.db import models
from django.utils import timezone

# Create your models here.


class User(models.Model):
    def __str__(self):
        return self.nickName

    openId = models.CharField(max_length=200)
    code = models.CharField(max_length=200)
    sessionKey = models.CharField(max_length=200)
    unionId = models.CharField(max_length=200)
    avatarUrl = models.CharField(max_length=200)
    city = models.CharField(max_length=200)
    country = models.CharField(max_length=200)
    gender = models.IntegerField(default=0)
    language = models.CharField(max_length=200)
    nickName = models.CharField(max_length=200)
    province = models.CharField(max_length=200)
    email = models.EmailField()
    createTime = models.DateTimeField(auto_now_add=True)


class Sentence(models.Model):
    def __str__(self):
        return self.content

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField(help_text='date submitted', default=timezone.now)
    content = models.TextField(help_text='sentence')
    createTime = models.DateTimeField(auto_now_add=True)


class Translate(models.Model):
    def __str__(self):
        return self.content

    sentence = models.ForeignKey(Sentence, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField(help_text='translate')
    createTime = models.DateTimeField(auto_now_add=True)
    numberOfLikes = models.IntegerField(default=0)
    numberOfComments = models.IntegerField(default=0)


class Comment(models.Model):
    def __str__(self):
        return self.content

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    translate = models.ForeignKey(Translate, on_delete=models.CASCADE)
    content = models.TextField(help_text='comment')
    createTime = models.DateTimeField(default=timezone.now)
