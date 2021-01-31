
from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.index, name="index"),
    path('login/', views.appLogin, name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('register/', views.appReg, name="register"),
    path('account/', views.accountDetails, name="account"),
    path('createserver/', views.createServer, name="createserver"),
]
