from django.urls import path

from music_app.views import *

urlpatterns = [
path('music/', MusicListView.as_view()),
path('music_create/', MusicCreateView.as_view()),
path('music_update/<int:pk>/', MusicUpdateView.as_view()),
path('music_detail/<int:pk>/', MusicDetailView.as_view()),
path('music_delete/<int:pk>/', MusicDeleteView.as_view()),
    ]