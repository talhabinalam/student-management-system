from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required


def user_login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, username=email, password=password)
        if user is not None:
            login(request, user)
            if user.user_type == 'HOD':
                return redirect('hod-home')
            elif user.user_type == 'STUDENT':
                return HttpResponse("This is STUDENT Dashboard")
            elif user.user_type == 'TEACHER':
                return HttpResponse('This is Teacher Dashboard')
            else:
                messages.error(request, "Invalid user type!")
                return redirect('login')
        else:
            messages.error(request, "Invalid email or password!")
            return redirect('login')
    return render(request, 'accounts/login.html')


@login_required
def user_logout(request):
    logout(request)
    return redirect('login')