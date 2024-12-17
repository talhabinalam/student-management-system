from django.shortcuts import render, redirect, get_object_or_404
from django.utils.dateparse import parse_date
from django.contrib import messages

from app.models import *


# ---------- Dashboard ----------

def home(request):
    """Render the home dashboard with statistics."""
    students = Student.objects.count()
    staffs = Staff.objects.count()
    courses = Course.objects.count()
    subjects = Subject.objects.count()

    # Gender-wise student count
    males = Student.objects.filter(gender='Male').count()
    females = Student.objects.filter(gender='Female').count()

    context = {
        'students': students,
        'staffs': staffs,
        'courses': courses,
        'subjects': subjects,
        'males': males,
        'females': females,
    }
    return render(request, 'hod/home.html', context)


# ---------- Student Management ----------

def add_student(request):
    """Add a new student and link them to a user."""
    courses = Course.objects.all()
    sessions = Session.objects.all()

    if request.method == 'POST':
        # Fetch form data
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        date_of_birth = request.POST.get('date_of_birth')
        email = request.POST.get('email')
        mobile = request.POST.get('mobile')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        address = request.POST.get('address')
        gender = request.POST.get('gender')
        course_id = request.POST.get('course_id')
        session_id = request.POST.get('session_id')

        # Validation
        if CustomUser.objects.filter(email=email).exists():
            messages.warning(request, "Email already exists!")
            return redirect('add_student')
        if password != confirm_password:
            messages.error(request, "Passwords do not match!")
            return redirect('add_student')

        # Create user and student records
        user = CustomUser(
            first_name=first_name,
            last_name=last_name,
            date_of_birth=date_of_birth,
            email=email,
            mobile=mobile,
            address=address,
            user_type='STUDENT'
        )
        user.set_password(password)
        user.save()

        course = get_object_or_404(Course, id=course_id)
        session = get_object_or_404(Session, id=session_id)

        student = Student(
            user=user,
            gender=gender,
            course=course,
            session=session
        )
        student.save()

        messages.success(request, "Student has been added successfully!")
        return redirect('student_list')

    context = {'courses': courses, 'sessions': sessions}
    return render(request, 'hod/add-student.html', context)


def student_list(request):
    """Display a list of all students."""
    students = Student.objects.all()
    return render(request, 'hod/student-list.html', {'students': students})


def student_details(request, id):
    """Show detailed information of a single student."""
    student = get_object_or_404(Student, id=id)
    return render(request, 'hod/student-details.html', {'student': student})


def update_student(request, id):
    """Update a student's information."""
    student = get_object_or_404(Student, id=id)
    user = student.user

    if request.method == 'POST':
        # Update user fields
        user.first_name = request.POST.get('first_name', user.first_name)
        user.last_name = request.POST.get('last_name', user.last_name)
        date_of_birth = parse_date(request.POST.get('date_of_birth', str(user.date_of_birth)))
        if date_of_birth:
            user.date_of_birth = date_of_birth
        user.email = request.POST.get('email', user.email)
        user.mobile = request.POST.get('mobile', user.mobile)
        user.address = request.POST.get('address', user.address)
        user.save()

        # Update student fields
        student.gender = request.POST.get('gender', student.gender)
        course_id = request.POST.get('course_id')
        session_id = request.POST.get('session_id')
        student.course = get_object_or_404(Course, id=course_id)
        student.session = get_object_or_404(Session, id=session_id)
        student.save()

        messages.success(request, "Student information updated successfully!")
        return redirect('student_list')

    courses = Course.objects.all()
    sessions = Session.objects.all()
    context = {'student': student, 'user': user, 'courses': courses, 'sessions': sessions}
    return render(request, 'hod/update-student.html', context)


def delete_student(request, id):
    """Delete a student and their associated user."""
    student = get_object_or_404(Student, id=id)
    student.user.delete()
    student.delete()
    messages.success(request, "Student deleted successfully!")
    return redirect('student_list')


# ---------- Staff Management ----------

def add_staff(request):
    """Add a new staff member."""
    if request.method == 'POST':
        # Fetch form data
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        date_of_birth = request.POST.get('date_of_birth')
        email = request.POST.get('email')
        mobile = request.POST.get('mobile')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        address = request.POST.get('address')
        gender = request.POST.get('gender')

        # Validation
        if CustomUser.objects.filter(email=email).exists():
            messages.warning(request, "Email already exists!")
            return redirect('add_staff')
        if password != confirm_password:
            messages.error(request, "Passwords do not match!")
            return redirect('add_staff')

        # Create user and staff records
        user = CustomUser(
            first_name=first_name,
            last_name=last_name,
            date_of_birth=date_of_birth,
            email=email,
            mobile=mobile,
            address=address,
            user_type="STAFF"
        )
        user.set_password(password)
        user.save()

        Staff.objects.create(user=user, gender=gender)
        messages.success(request, "Staff member added successfully!")
        return redirect('staff_list')

    return render(request, 'hod/add-staff.html')


def staff_list(request):
    staffs = Staff.objects.all()
    return render(request, 'hod/staff-list.html', {'staffs':staffs})


def staff_details(request, id):
    staff = Staff.objects.get(id=id)
    return render(request, 'hod/staff-details.html', {'staff':staff})


def update_staff(request, id):
    """Update staff member details."""
    staff = get_object_or_404(Staff, id=id)
    user = staff.user

    if request.method == 'POST':
        user.first_name = request.POST.get('first_name', user.first_name)
        user.last_name = request.POST.get('last_name', user.last_name)
        user.date_of_birth = request.POST.get('date_of_birth', user.date_of_birth)
        user.email = request.POST.get('email', user.email)
        user.mobile = request.POST.get('mobile', user.mobile)
        user.address = request.POST.get('address', user.address)
        user.save()

        staff.gender = request.POST.get('gender', staff.gender)
        staff.save()
        messages.success(request, "Staff updated successfully!")
        return redirect('staff_list')

    return render(request, 'hod/update-staff.html', {'staff': staff, 'user': user})


def delete_staff(request, id):
    staff = Staff.objects.get(id=id)
    staff.delete()
    staff.user.delete()
    messages.success(request, "Staff has been deleted!")
    return redirect('staff_list')


# ---------- Course Management ----------

def add_course(request):
    """Add a new course."""
    if request.method == 'POST':
        course_name = request.POST.get('course')

        if Course.objects.filter(name__iexact=course_name).exists():
            messages.warning(request, "Course already exists!")
            return redirect('add_course')

        Course.objects.create(name=course_name)
        messages.success(request, "Course added successfully!")
        return redirect('course_list')
    return render(request, 'hod/add-course.html')


def course_list(request):
    """List all courses."""
    courses = Course.objects.all()
    return render(request, 'hod/course-list.html', {'courses': courses})


def update_course(request, id):
    """Update a course."""
    course = get_object_or_404(Course, id=id)
    if request.method == 'POST':
        course.name = request.POST.get('name', course.name)
        course.save()
        messages.success(request, "Course updated successfully!")
        return redirect('course_list')
    return render(request, 'hod/update-course.html', {'course': course})


def delete_course(request, id):
    """Delete a course if no students are assigned to it."""
    course = get_object_or_404(Course, id=id)
    if Student.objects.filter(course=course).exists():
        messages.error(request, "Cannot delete course with assigned students.")
        return redirect('course_list')
    course.delete()
    messages.success(request, "Course deleted successfully!")
    return redirect('course_list')



# ---------- Subject Management ----------

def add_subject(request):
    """Add a new subject and associate it with a course and staff."""
    courses = Course.objects.all()  # Fetch all available courses
    staffs = Staff.objects.all()  # Fetch all available staff members

    if request.method == 'POST':
        # Retrieve form data
        name = request.POST.get('name')
        course_id = request.POST.get('course_id')
        staff_id = request.POST.get('staff_id')

        # Fetch the related course and staff objects
        course = get_object_or_404(Course, id=course_id)
        staff = get_object_or_404(Staff, id=staff_id)

        # Create and save the new subject
        subject = Subject(name=name, course=course, staff=staff)
        subject.save()

        # Show success message
        messages.success(request, "Subject has been added!")
        return redirect('subject_list')

    # Pass context data to the template
    context = {'courses': courses, 'staffs': staffs}
    return render(request, 'hod/add-subject.html', context)


def subject_list(request):
    """Display a list of all subjects."""
    subjects = Subject.objects.all()  # Fetch all subjects from the database
    return render(request, 'hod/subject-list.html', {'subjects': subjects})


def update_subject(request, id):
    """Update an existing subject."""
    subject = get_object_or_404(Subject, id=id)  # Fetch subject by ID
    courses = Course.objects.all()  # Fetch all available courses
    staffs = Staff.objects.all()  # Fetch all available staff members

    if request.method == 'POST':
        # Update subject details from the form data
        subject.name = request.POST.get('name', subject.name)
        course_id = request.POST.get('course_id', subject.course.id)
        staff_id = request.POST.get('staff_id', subject.staff.id)

        # Fetch updated course and staff
        subject.course = get_object_or_404(Course, id=course_id)
        subject.staff = get_object_or_404(Staff, id=staff_id)

        # Save the updated subject
        subject.save()

        # Show success message
        messages.success(request, "Subject has been updated!")
        return redirect('subject_list')

    # Pass context data to the template for rendering the form
    context = {'subject': subject, 'courses': courses, 'staffs': staffs}
    return render(request, 'hod/update_subject.html', context)


def delete_subject(request, id):
    """Delete a subject from the database."""
    subject = get_object_or_404(Subject, id=id)
    subject.delete()  # Delete the subject from the database
    messages.success(request, "Subject has been deleted!")
    return redirect('subject_list')



# ---------- Session Management ----------

def add_session(request):
    """Add a new session."""
    if request.method == 'POST':
        session_start = request.POST.get('session_start')
        session_end = request.POST.get('session_end')

        # Check if a session already exists for the given start year
        if Session.objects.filter(session_start=session_start).exists():
            messages.error(request, "Session already exists!")
            return redirect('add_session')

        # Create and save the new session
        session = Session(session_start=session_start, session_end=session_end)
        session.save()

        # Show success message
        messages.success(request, "Session has been added!")
        return redirect('session_list')

    return render(request, 'hod/add-session.html')


def session_list(request):
    """Display a list of all sessions."""
    sessions = Session.objects.all()  # Fetch all sessions from the database
    return render(request, 'hod/session-list.html', {'sessions': sessions})


def update_session(request, id):
    """Update an existing session."""
    session = get_object_or_404(Session, id=id)  # Fetch session by ID

    if request.method == 'POST':
        # Update session details from the form data
        session.session_start = request.POST.get('session_start', session.session_start)
        session.session_end = request.POST.get('session_end', session.session_end)

        # Save the updated session
        session.save()

        # Show success message
        messages.success(request, "Session updated!")
        return redirect('session_list')

    return render(request, 'hod/update-session.html', {'session': session})


def delete_session(request, id):
    """Delete a session if no students are linked to it."""
    session = get_object_or_404(Session, id=id)

    # Check if there are students linked to this session
    if Student.objects.filter(session=session).exists():
        messages.warning(request, "This session contains students!")
        return redirect('session_list')

    # Delete the session if no students are linked
    session.delete()
    messages.success(request, "Session deleted!")
    return redirect('session_list')



# ---------- Notification Management ----------

def send_staff_notification(request):
    """Display a page to send notifications to staff."""
    staffs = Staff.objects.all()  # Fetch all staff members
    notifications = StaffNotification.objects.order_by('-created_at')[:8]  # Fetch the most recent 8 notifications

    # Pass staff and notification data to the template
    context = {'staffs': staffs, 'notifications': notifications}
    return render(request, 'hod/send-staff-notification.html', context)


def save_staff_notification(request):
    """Save and send a notification to a selected staff member."""
    if request.method == 'POST':
        staff_id = request.POST.get('staff_id')
        message = request.POST.get('message')

        # Fetch the selected staff member
        staff = get_object_or_404(Staff, user=staff_id)

        # Create and save the notification
        notification = StaffNotification(staff=staff, message=message)
        notification.save()

        # Show success message
        messages.success(request, "Message has been sent!")
        return redirect('send_staff_notification')


def send_student_notification(request):
    """Display a page to send notifications to students."""
    students = Student.objects.all()  # Fetch all students
    notifications = StudentNotification.objects.all().order_by('-created_at')[:8]  # Fetch the most recent 8 notifications

    # Pass student and notification data to the template
    context = {'students': students, 'notifications': notifications}
    return render(request, 'hod/send_student_notification.html', context)


def save_student_notification(request):
    """Save and send a notification to a selected student."""
    if request.method == 'POST':
        student_id = request.POST.get('student_id')
        message = request.POST.get('message')

        # Fetch the selected student
        student = get_object_or_404(Student, id=student_id)

        # Create and save the notification
        student_notification = StudentNotification(student=student, message=message)
        student_notification.save()

        # Show success message
        messages.success(request, "Notification has been sent to the student!")
        return redirect('send_student_notification')



# ---------- Leave Management ----------

def staff_leave(request):
    """Display a list of staff leave requests."""
    staffs = StaffLeave.objects.all()  # Fetch all staff leave records
    return render(request, 'hod/staff-leave.html', {'staffs': staffs})


def staff_approve_leave(request, id):
    """Approve a staff leave request."""
    staff_leave = get_object_or_404(StaffLeave, id=id)
    staff_leave.status = 1  # Set the leave status to approved
    staff_leave.save()
    return redirect('staff_leave')


def staff_decline_leave(request, id):
    """Decline a staff leave request."""
    staff_leave = get_object_or_404(StaffLeave, id=id)
    staff_leave.status = 2  # Set the leave status to declined
    staff_leave.save()
    return redirect('staff_leave')


def student_leave(request):
    """Display a list of student leave requests."""
    students = StudentLeave.objects.all()  # Fetch all student leave records
    return render(request, 'hod/student-leave.html', {'students': students})


def student_approve_leave(request, id):
    """Approve a student leave request."""
    student_leave = get_object_or_404(StudentLeave, id=id)
    student_leave.status = 1  # Set the leave status to approved
    student_leave.save()
    return redirect('student_leave')


def student_decline_leave(request, id):
    """Decline a student leave request."""
    student_leave = get_object_or_404(StudentLeave, id=id)
    student_leave.status = 2  # Set the leave status to declined
    student_leave.save()
    return redirect('student_leave')


# ---------- Feedback Management ----------

def staff_feedback_replay(request):
    """Handle staff feedback replies."""
    if request.method == 'POST':
        # Retrieve the feedback ID and the reply message from the form
        feedback_id = request.POST.get('feedback_id')
        feedback_replay = request.POST.get('feedback_replay')

        # Fetch the corresponding feedback record from the StaffFeedback table
        try:
            feedback = StaffFeedback.objects.get(id=feedback_id)
        except StaffFeedback.DoesNotExist:
            messages.error(request, "Feedback not found!")
            return redirect('staff_feedback_replay')

        # Update feedback reply and mark it as replied
        feedback.feedback_replay = feedback_replay
        feedback.is_replied = True
        feedback.save()

        # Show success message
        messages.success(request, "Feedback reply sent successfully!")
        return redirect('staff_feedback_replay')

    # Fetch all feedback records to display in the template
    staff_feedback = StaffFeedback.objects.all().order_by('-created_at')[:8]
    context = {
        'staff_feedback': staff_feedback,
    }
    return render(request, 'hod/staff-feedback-replay.html', context)


def student_feedback_replay(request):
    """Handle student feedback replies."""
    if request.method == 'POST':
        # Retrieve the feedback ID and the reply message from the form
        feedback_replay = request.POST.get('feedback_replay')
        feedback_id = request.POST.get('feedback_id')

        # Fetch the corresponding feedback record from the StudentFeedback table
        try:
            student_feedback = StudentFeedback.objects.get(id=feedback_id)
        except StudentFeedback.DoesNotExist:
            messages.error(request, "Feedback not found!")
            return redirect('student_feedback_replay')

        # Update feedback reply and mark it as replied
        student_feedback.feedback_replay = feedback_replay
        student_feedback.is_replied = True
        student_feedback.save()

        # Show success message
        messages.success(request, "Replay has been sent successfully!")
        return redirect('student_feedback_replay')

    # Fetch all student feedback records to display in the template
    student_feedback = StudentFeedback.objects.all()
    context = {
        'student_feedback': student_feedback,
    }
    return render(request, 'hod/student-feedback-replay.html', context)



def hod_view_attendance(request):
    subjects = Subject.objects.all()
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

    return render(request, 'hod/view-attendance.html', context)