from django.shortcuts import render, redirect
from django.contrib import messages

from app.models import *


def home(request):
    return render(request, 'staff/home.html')


def staff_notification(request):
    staff = Staff.objects.filter(user=request.user.id)

    for i in staff:
        staff_id = i.id
        notifications = StaffNotification.objects.filter(staff=staff_id)

    context = {
        'notifications':notifications,
    }

    return render(request, 'staff/notification.html', context)


def staff_msg_status(request, id):
    notification = StaffNotification.objects.get(id=id)
    notification.status = 1
    notification.save()
    return redirect('staff_notification')


def staff_leave(request):
    return render(request, 'staff/staff-leave.html')