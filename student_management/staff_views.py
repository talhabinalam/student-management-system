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


def apply_staff_leave(request):
    if request.method == 'POST':
        subject = request.POST.get('subject')
        date = request.POST.get('date')
        message = request.POST.get('message')

        staff = Staff.objects.get(user=request.user)

        leave = StaffLeave(
            staff=staff,
            subject=subject,
            date=date,
            message=message,
        )
        leave.save()
        messages.success(request, "Leave application has been sent!")
        return redirect('apply_staff_leave')

    staff_id = Staff.objects.filter(user=request.user.id)
    for i in staff_id:
        staff = i.id
        leave_history = StaffLeave.objects.filter(staff=staff)

    context = {
        'leave_history':leave_history,
    }

    return render(request, 'staff/staff-leave.html', context)

