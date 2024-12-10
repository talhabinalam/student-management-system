from django.shortcuts import render, redirect
from django.contrib import messages



def home(request):
    return render(request, 'staff/home.html')


def notification(request):
    return render(request, 'staff/notification.html')