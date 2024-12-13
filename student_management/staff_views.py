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


def staff_notification_status(request, id):
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

    #Getch the queryset by filtering user
    staff_id = Staff.objects.filter(user=request.user.id)
    for i in staff_id:
        staff = i.id
        leave_history = StaffLeave.objects.filter(staff=staff)

    context = {
        'leave_history':leave_history,
    }
    return render(request, 'staff/staff-leave.html', context)



def staff_feedback(request):
    if request.method == 'POST':
        feedback = request.POST.get('feedback')

        #Fetch the requested staff using foreignkey
        staff = Staff.objects.get(user=request.user.id)
        feedback = StaffFeedback(
            staff=staff,
            feedback=feedback,
            feedback_replay="",
        )
        feedback.save()
        messages.success(request, "Feedback has been sent!")
        return redirect('staff_feedback')

    staff = Staff.objects.get(user=request.user.id)
    feedbacks = StaffFeedback.objects.filter(staff=staff)

    context = {
        'feedbacks':feedbacks,
    }
    return render(request, 'staff/staff-feedback.html', context)

