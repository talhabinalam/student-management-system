from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.views import View
from django.contrib import messages

from app.models import *


def home(request):
    return render(request, "student/home.html")


def student_notification(request):
    student = Student.objects.get(user=request.user)
    notifications = StudentNotification.objects.filter(student=student)

    context = {
        'notifications':notifications
    }
    return render(request, 'student/notification.html', context)


def student_notification_status(request, id):
    notification = StudentNotification.objects.get(id=id)
    notification.status = 1
    notification.save()
    return redirect('student_notification')


def student_feedback(request):
    if request.method == 'POST':
        feedback = request.POST.get('feedback')
        student = Student.objects.get(user=request.user.id)
        stu_feedback = StudentFeedback(
            student=student,
            feedback=feedback,
            feedback_replay="",
        )
        stu_feedback.save()
        messages.success(request, "Feedback has been sent!")
        return redirect('student_feedback')

    student = Student.objects.get(user=request.user.id)
    feedbacks = StudentFeedback.objects.filter(student=student)

    return render(request, 'student/student-feedback.html', {'feedbacks':feedbacks})


def apply_student_leave(request):
    if request.method == 'POST':
        subject = request.POST.get('subject')
        date = request.POST.get('date')
        message = request.POST.get('message')

        student = Student.objects.get(user=request.user.id)

        student_leave = StudentLeave(
            student=student,
            subject=subject,
            date=date,
            message=message,
        )
        student_leave.save()
        messages.success(request, "Leave application has been sent!")
        return redirect('apply_student_leave')

    student = Student.objects.get(user=request.user.id)
    student_leave = StudentLeave.objects.filter(student=student)

    context = {
        'student_leave':student_leave
    }
    return render(request, 'student/student-leave.html', context)