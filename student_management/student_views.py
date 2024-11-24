from django.shortcuts import render, redirect

def base(request):
    return render(request, 'base.html')


def login(request):
    return render(request, 'accounts/login.html')