from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.views import View


def base(request):
    return render(request, 'base.html')


class LoginView(View):
    def get(self, request):
        return render(request, 'accounts/login.html')

    def post(self, request):
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, email=email, password=password)
        print(user)
        if user is not None:
            login(request, user)

            if user.user_type == 'HOD':
                return HttpResponse("This is HOD Dashboard")
            elif user.user_type == 'STUDENT':
                return HttpResponse("This is STUDENT Dashboard")
            elif user.user_type == 'TEACHER':
                return HttpResponse('This is Teacher Dashboard')
            else:
                return HttpResponse('User not matched')
        else:
            return HttpResponse('Invalid email or password')

