from django.urls import path
from . import views

urlpatterns = [
    path('chat/test/', views.testsubmit, name='testsubmit'),

    path('api/gpt_chat/', views.chat, name='chat'),

    path('chat/', views.chat_view, name='chat_view'),
    
   
]
