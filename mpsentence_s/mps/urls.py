from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('<int:date_id>/', views.daily_sentence, name='daily_sentence'),
    path('openId/get/', views.get_openid, name='get_openid'),
    path('user/register', views.user_register, name='user_register'),
    path('sentence', views.sentence, name='sentence'),
    path('translate', views.translate, name='translate'),
    path('translate/update', views.translate_update, name='translate_update'),
]
