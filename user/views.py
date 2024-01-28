from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from adminUser.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import Todo
from django.contrib import messages

def userHome(request):
    return render(request, 'userHome.html')

#Registration view
def userRegister(request):
    if request.method == 'POST':
        firstname = request.POST.get('firstname')
        lastname = request.POST.get('lastname')
        username = request.POST.get('username')
        gender = request.POST.get('gender')
        email = request.POST.get('email').lower()
        phone = request.POST.get('phone')
        address = request.POST.get('address')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        
        # Validating registration
        if password != confirm_password:
            return HttpResponse("password does'nt match")
        elif User.objects.filter(email=email).exists():
            return HttpResponse("Email already exist")
        elif User.objects.filter(username=username).exists():
            return HttpResponse("Username already exist")
        else:
            user = User.objects.create(username=username, email=email, gender=gender, phone=phone, address=address, first_name = firstname, last_name = lastname)
            user.set_password(password)
            user.save()
            return redirect('login')
        # End of validating 
        
            # Passwords don't match, handle this case (redirect to the registration page with an error message)
            # error_message = "Passwords don't match. Please try again."
            # return render(request, 'adminRegister.html', {'error_message': error_message})
    return render(request, 'userRegister.html')

#Login view
def userLogin(request):
    if request.method == 'POST':
        email = request.POST.get('email').lower()
        password = request.POST.get('password')
        user = authenticate(email=email, password=password)
        if user is not None:
            if user.is_superuser:
                return redirect('admin:login')
            else:
                login(request, user)
                return redirect('todo')
        else:
            return HttpResponse('Mismatched credentials')
    return render(request, 'userLogin.html')

#Loged in view
@login_required(login_url='login')
def userTodo(request):
    user = request.user
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        due_date = request.POST.get('due_date')
        priority = request.POST.get('priority')
        status = request.POST.get('status')
        if Todo.objects.filter(author=user, title=title).exists():
            return HttpResponse('You already created a task with title called ' + title.upper())
        else:
            task = Todo.objects.create(author=user,title=title,description=description,due_date=due_date,priority=priority,status=status)
            task.save()
            return redirect('tasklist')
    return render(request, 'userTodo.html', context={'User':user})

# Logout view
def userLogout(request):
    logout(request)
    return redirect('login')

# task_list
@login_required(login_url='login')
def userTask(request):
    userTodo = Todo.objects.filter(author=request.user)
    return render(request, 'userTaskView.html', {'todos':userTodo})

@login_required(login_url='login')
def userTaskDetail(request, id):
    taskDetail = Todo.objects.get(id=id)
    return render(request, 'userTaskDetail.html', {'taskDetail':taskDetail}) 

@login_required(login_url='login')
def updateUserTodo(request, id):
    user = request.user
    taskUpdate = Todo.objects.get(id=id)
    if request.method == 'POST':
        taskUpdate.title = request.POST.get('title')
        taskUpdate.description = request.POST.get('description')
        taskUpdate.priority = request.POST.get('priority')
        taskUpdate.status = request.POST.get('status')
        taskUpdate.save()
        return redirect('userTaskDetail', id=id)
    return render(request, 'updateUserTodo.html', {'taskUpdate': taskUpdate}) 

@login_required(login_url='login')
def taskDelete(request, id):
    taskDetail = get_object_or_404(Todo, id=id)
    taskDetail.delete()
    return redirect('tasklist')
