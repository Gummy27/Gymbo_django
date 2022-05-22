from django.urls import path
from . import views

urlpatterns = [
    path('signin', views.signin, name='signin'),
    path('signup', views.signup, name='signup'),
    path('logout', views.signout, name='signout'),
    path('change', views.change, name='change'),
    path('update', views.update, name='update'),
]
