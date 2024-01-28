from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from .models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

def adminHome(request):
    return render(request, 'adminHome.html')

#Registration view
def adminRegister(request):
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
            user.is_staff = True
            user.is_superuser = True
            user.set_password(password)  
            user.save()
            return redirect('admin:login')
        # End of validating 
        
            # Passwords don't match, handle this case (redirect to the registration page with an error message)
            # error_message = "Passwords don't match. Please try again."
            # return render(request, 'adminRegister.html', {'error_message': error_message})
    return render(request, 'adminRegister.html')

#Login view
def adminLogin(request):
    if request.method == 'POST':
        email = request.POST.get('email').lower()
        password = request.POST.get('password')
        user = authenticate(email=email, password=password)
        if user is not None:
            if user.is_superuser:
                login(request, user)
                return redirect('admin:logedin')
            else:
                return redirect('login')
        else:
            return HttpResponse('Mismatched credentials')
    return render(request, 'adminLogin.html')

#Loged in view
@login_required(login_url = 'admin:login')
def adminLogedin(request):
    user = request.user
    users = User.objects.all()
    return render(request, 'adminLogedIn.html', context={'users':users, 'adminuser':user})

@login_required
def adminLogout(request):
    logout(request)
    return redirect('admin:login')

# @login_required
def userDelete(request, id):
    taskDetail = get_object_or_404(User, id=id)
    taskDetail.delete()
    return redirect('admin:logedin')