from django.urls import path
from . import views

urlpatterns = [
    path('home', views.home, name='home'),
    path('exercises', views.exercises, name='exercises'),
    path('detailed/<int:exercise_id>', views.detailed, name='detailed'),
    path('overview', views.current_session, name='current_session')
]
