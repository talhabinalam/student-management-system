from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.contrib import messages

from app.models import *


def home(request):
    staff = Staff.objects.get(user=request.user)
    notifications = StaffNotification.objects.filter(staff=staff).order_by('-created_at')[:5]  # Show recent 5
    context = {
        'notifications':notifications,
    }
    return render(request, 'staff/home.html', context)


def staff_notification(request):
    """Display notifications for the logged-in staff."""
    staff = get_object_or_404(Staff, user=request.user)
    notifications = StaffNotification.objects.filter(staff=staff)
    context = {'notifications': notifications}
    return render(request, 'staff/notification.html', context)



def staff_notification_status(request, id):
    """Mark a notification as read."""
    notification = get_object_or_404(StaffNotification, id=id)
    notification.status = 1
    notification.save()
    return redirect('staff_notification')


def apply_staff_leave(request):
    """Handle leave applications and display leave history."""
    staff = get_object_or_404(Staff, user=request.user)

    if request.method == 'POST':
        subject = request.POST.get('subject')
        date = request.POST.get('date')
        message = request.POST.get('message')

        StaffLeave.objects.create(
            staff=staff,
            subject=subject,
            date=date,
            message=message
        )
        messages.success(request, "Leave application has been sent!")
        return redirect('apply_staff_leave')

    leave_history = StaffLeave.objects.filter(staff=staff)
    context = {'leave_history': leave_history}
    return render(request, 'staff/staff-leave.html', context)


def staff_feedback(request):
    """Handle staff feedback submission and display history."""
    staff = get_object_or_404(Staff, user=request.user)

    if request.method == 'POST':
        feedback_content = request.POST.get('feedback')
        StaffFeedback.objects.create(
            staff=staff,
            feedback=feedback_content,
            feedback_replay=""
        )
        messages.success(request, "Feedback has been sent!")
        return redirect('staff_feedback')

    feedbacks = StaffFeedback.objects.filter(staff=staff)
    context = {'feedbacks': feedbacks}
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
        students = Student.objects.filter(course=get_subject.course, session=get_session)

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
        student_ids = request.POST.getlist('student_id')  # List of student IDs

        # Fetch Subject and Session objects
        subject = get_object_or_404(Subject, id=subject_id)
        session = get_object_or_404(Session, id=session_id)

        # Create Attendance record
        attendance = Attendance.objects.create(
            subject=subject,
            session=session,
            date=date
        )

        # Bulk create AttendanceReport records
        attendance_reports = [
            AttendanceReport(student_id=student_id, attendance=attendance)
            for student_id in student_ids
        ]
        AttendanceReport.objects.bulk_create(attendance_reports)

        # Add success message and redirect
        messages.success(request, "Attendance has been taken successfully!")
        return redirect('staff_take_attendance')



def staff_view_attendance(request):
    staff = Staff.objects.get(user=request.user)
    subjects = Subject.objects.filter(staff=staff)
    sessions = Session.objects.all()

    action = request.GET.get('action')

    get_subject = None
    get_session = None
    date = None
    attendance_report = None

    if action is not None:
        if request.method == 'POST':
            subject_id = request.POST.get('subject')
            session_id = request.POST.get('session')
            date = request.POST.get('date')

            # Get the selected subject and session
            get_subject = Subject.objects.get(id=subject_id)
            get_session = Session.objects.get(id=session_id)

            # Get the Attendance object for the given subject and date
            attendance = Attendance.objects.filter(subject=get_subject, session=get_session, date=date).first()

            # If attendance exists, fetch related AttendanceReport
            if attendance:
                attendance_report = AttendanceReport.objects.filter(attendance=attendance)

    context = {
        'subjects': subjects,
        'sessions': sessions,
        'action': action,
        'get_subject': get_subject,
        'get_session': get_session,
        'date': date,
        'attendance_report': attendance_report,
    }

    return render(request, 'staff/view-attendance.html', context)


def add_result(request):
    staff = Staff.objects.get(user=request.user)
    subjects = Subject.objects.filter(staff=staff)
    sessions = Session.objects.all()

    action = request.GET.get('action')

    get_subject = None
    get_session = None
    students = None

    if action is not None:
        if request.method == 'POST':
            subject_id = request.POST.get('subject_id')
            session_id = request.POST.get('session_id')

            get_subject = Subject.objects.get(id=subject_id)
            get_session = Session.objects.get(id=session_id)

            students = Student.objects.filter(course=get_subject.course, session=get_session)

    context = {
        'subjects':subjects,
        'sessions':sessions,
        'action':action,
        'get_subject':get_subject,
        'get_session':get_session,
        'students':students,

    }

    return render(request, 'staff/add-result.html', context)


def save_result(request):
    if request.method == 'POST':
        student_id = request.POST.get('student_id')
        subject = request.POST.get('subject')
        quiz_mark = request.POST.get('quiz_mark')
        exam_mark = request.POST.get('exam_mark')

        subject = Subject.objects.get(name=subject)
        student = Student.objects.get(id=student_id)

        StudentResult.objects.create(
            student=student, subject=subject, quiz_mark=quiz_mark, exam_mark=exam_mark
        )
        messages.success(request, "Result has been added!")
        return redirect('add_result')
