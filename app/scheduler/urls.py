

from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('schedule/', views.schedule),
    path('show_schedule/', views.show_schedule, name='show_schedule'),
    path('learn_more/', views.learn_more, name='learn_more'),
]
