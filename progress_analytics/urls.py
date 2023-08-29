from django.urls import path
from . import views

urlpatterns = [

    path('exercise/', views.exercise, name='exercise'),
    path('clear_session/', views.clear_session, name='clear_session'),
    path('get_energy_points/', views.get_energy_points, name='get_energy_points'),

]
