from django.urls import path
from . import views as admin

app_name = 'admin'
urlpatterns = [
    path('', admin.adminHome, name = 'home'),
    path('register', admin.adminRegister, name = 'register'),
    path('login', admin.adminLogin, name = 'login'),
    path('logedin', admin.adminLogedin, name = 'logedin'),
    path('logout', admin.adminLogout, name='logout'),
    path('userDelete/<int:id>', admin.userDelete, name='userDelete')
]