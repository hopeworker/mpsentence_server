from django.contrib import admin

# Register your models here.
from .models import User, Sentence, Translate, Comment

admin.site.register(User)
admin.site.register(Sentence)
admin.site.register(Translate)
admin.site.register(Comment)
