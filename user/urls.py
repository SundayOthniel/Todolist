from django.urls import path
from . import views as user

urlpatterns = [
    path('', user.userHome, name = 'home'),
    path('register', user.userRegister, name = 'register'),
    path('login', user.userLogin, name = 'login'),
    path('todo', user.userTodo, name = 'todo'),
    path('logout', user.userLogout, name='logout'),
    path('tasklist', user.userTask, name='tasklist'),
    path('TaskDetail/<int:id>', user.userTaskDetail, name='userTaskDetail'), 
    path('updatetask/<int:id>', user.updateUserTodo, name='updatetask'),
    path('taskDelete/<int:id>', user.taskDelete, name='taskDelete'),
]