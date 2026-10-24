from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('section/<slug:slug>/', views.section_detail, name='section'),
    path('quiz/', views.quiz, name='quiz'),
    path('quests/', views.quest_list, name='quest_list'),
    path('quest/<slug:slug>/', views.quest_detail, name='quest_detail'),
    path('quest/<slug:slug>/scene/<int:scene_id>/', views.quest_scene, name='quest_scene'),
]