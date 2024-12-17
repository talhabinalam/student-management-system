from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages

from app.models import *


def home(request):
    return render(request, "student/home.html")


# View to display notifications for the logged-in student
def student_notification(request):
    # Fetch the student record for the logged-in user
    student = Student.objects.get(user=request.user)

    # Get all notifications for this student
    notifications = StudentNotification.objects.filter(student=student)

    # Pass notifications to the template
    context = {
        'notifications': notifications
    }
    return render(request, 'student/notification.html', context)


# View to update the status of a notification to "read"
def student_notification_status(request, id):
    # Get the notification by its ID
    notification = StudentNotification.objects.get(id=id)

    # Update the notification's status to 1 (read)
    notification.status = 1
    notification.save()

    # Redirect back to the notifications page
    return redirect('student_notification')


# View for student feedback submission
def student_feedback(request):
    if request.method == 'POST':
        # Get feedback content from the form
        feedback = request.POST.get('feedback')

        # Fetch the student record for the logged-in user
        student = Student.objects.get(user=request.user.id)

        # Save the feedback to the database
        stu_feedback = StudentFeedback(
            student=student,
            feedback=feedback,
            feedback_replay="",
        )
        stu_feedback.save()

        # Show success message and redirect to feedback page
        messages.success(request, "Feedback has been sent!")
        return redirect('student_feedback')

    # Get all feedbacks submitted by the student
    student = Student.objects.get(user=request.user.id)
    feedbacks = StudentFeedback.objects.filter(student=student)

    # Pass feedbacks to the template
    return render(request, 'student/student-feedback.html', {'feedbacks': feedbacks})


# View to apply for student leave
def apply_student_leave(request):
    if request.method == 'POST':
        # Get leave application details from the form
        subject = request.POST.get('subject')
        date = request.POST.get('date')
        message = request.POST.get('message')

        # Fetch the student record for the logged-in user
        student = Student.objects.get(user=request.user.id)

        # Save the leave application to the database
        student_leave = StudentLeave(
            student=student,
            subject=subject,
            date=date,
            message=message,
        )
        student_leave.save()

        # Show success message and redirect to leave application page
        messages.success(request, "Leave application has been sent!")
        return redirect('apply_student_leave')

    # Fetch all leave applications of the student
    student = Student.objects.get(user=request.user.id)
    student_leave = StudentLeave.objects.filter(student=student)

    # Pass leave applications to the template
    context = {
        'student_leave': student_leave
    }
    return render(request, 'student/student-leave.html', context)


def student_view_attendance(request):
    student = Student.objects.get(user=request.user)
    subjects = Subject.objects.filter(course=student.course)

    action = request.GET.get('action')

    get_subject = None
    attendance_report = None

    if action is not None:
        if request.method == 'POST':
            subject_id = request.POST.get('subject_id')
            get_subject = Subject.objects.get(id=subject_id)

            #Fetching attendance report of logged-in user
            attendance_report = AttendanceReport.objects.filter(student=student, attendance__subject=subject_id)

    context = {
        'subjects':subjects,
        'action':action,
        'get_subject':get_subject,
        'attendance_report':attendance_report,
    }
    return render(request, 'student/view-attendance.html', context)


def view_result(request):
    student = Student.objects.get(user=request.user)
    student_result = StudentResult.objects.filter(student=student)

    marks = None
    for i in student_result:
        quiz = i.quiz_mark
        exam = i.exam_mark
        marks = quiz + exam

    context = {
        'student_result':student_result,
        'marks':marks,
    }
    return render(request, 'student/view-result.html', context)