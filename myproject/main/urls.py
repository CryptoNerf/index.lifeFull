from django.urls import path
from . import views

urlpatterns = [
    path('moods/', views.mood_grid, name='mood_grid'),
    path('register/', views.register, name='register'),
    path('day/<str:day>/', views.edit_day, name='edit_day'),
    path('account/', views.account, name='account'),
]
