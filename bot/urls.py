from django.urls import path

from . import views

urlpatterns = [
    path('bot/faq/<str:room_name>', views.index, name='index'),
    path('', views.bot, name='faq'),
    path('bbott', views.bbott, name='bbott')

]
