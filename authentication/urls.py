from django.urls import path
from . import views


urlpatterns = [
    path('', views.login_user, name='login'),
    path('home', views.home, name='home'),
    path('registro', views.register, name='register'),
    path('login', views.login_user, name='login'),
    path('logout_user', views.logout_user, name='logout_user'),
    path('activate-user/<uidb64>/<token>', views.activate_user, name='activate'),
    path('alterar-senha', views.password_change, name='password_change'),
]