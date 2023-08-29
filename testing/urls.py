from django.urls import path
from . import views

urlpatterns = [
    # path('chat/test/', views.testsubmit, name='testsubmit'),

    # path('api/gpt_chat/', views.chat, name='chat'),

    path('chat/', views.chat_view, name='chat_view'),

    # this one below is used for functiom calling route, and is accesed by a form in chat.html
    path('chat/', views.weather_request, name='weather_request'),


]
