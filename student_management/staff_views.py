from django.shortcuts import render, redirect, get_object_or_404
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

    leave_history = None
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


def staff_take_attendance(request):
    # Fetch the staff object associated with the logged-in user
    staff = get_object_or_404(Staff, user=request.user.id)

    # Retrieve subjects and sessions
    subjects = Subject.objects.filter(staff=staff)
    sessions = Session.objects.all()

    # Initialize variables for template context
    get_subject = None
    get_session = None
    students = None
    action = request.GET.get('action')

    if action and request.method == 'POST':
        subject_id = request.POST.get('subject_id')
        session_id = request.POST.get('session_id')

        # Fetch subject and session using the provided IDs
        get_subject = get_object_or_404(Subject, id=subject_id)
        get_session = get_object_or_404(Session, id=session_id)

        # Retrieve students enrolled in the course related to the subject
        students = Student.objects.filter(course=get_subject.course)

    # Prepare context for the template
    context = {
        'subjects': subjects,
        'sessions': sessions,
        'get_subject': get_subject,
        'get_session': get_session,
        'action': action,
        'students': students,
    }

    return render(request, 'staff/take-attendance.html', context)



def staff_save_attendance(request):
    if request.method == 'POST':
        subject_id = request.POST.get('subject_id')
        session_id = request.POST.get('session_id')
        date = request.POST.get('date')
        student_id = request.POST.getlist('student_id')

        print(subject_id)
        print(session_id)

        get_subject = Subject.objects.get(id=subject_id)
        get_session = Session.objects.get(id=session_id)

        attendance = Attendance(
            subject=get_subject,
            session=get_session,
            date=date,
        )
        attendance.save()

        for student in student_id:
            stu_id = student
            int_stu = int(stu_id)

            preset_stu = Student.objects.get(id=int_stu)
            attendance_report = AttendanceReport(
                student=preset_stu,
                attendance=attendance,
            )
            attendance_report.save()
    messages.success(request, "Attendance has been taken!")
    return redirect('staff_take_attendance')




