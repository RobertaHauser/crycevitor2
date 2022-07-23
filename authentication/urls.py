from django.urls import path, include
from . import views


urlpatterns = [
    path('', views.home, name='home'),
    path('home', views.home, name='home'),
    path('registro', views.register, name='register'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('activate-user/<uidb64>/<token>', views.activate_user, name='activate'),
]