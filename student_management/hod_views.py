from django.shortcuts import render, redirect, get_object_or_404
from django.utils.dateparse import parse_date
from django.contrib import messages

from app.models import *


def home(request):
    return render(request, 'hod/home.html')


def add_student(request):
    courses = Course.objects.all()
    sessions = Session.objects.all()

    if request.method == 'POST':
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

        if studentUser.objects.filter(email=email).exists():
            messages.warning(request, "Email already exists!")
            return redirect('add_student')

        if password != confirm_password:
            messages.error(request, "Password did not match!")
            return redirect('add_student')

        user = studentUser(
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

        course = Course.objects.get(id=course_id)
        session = Session.objects.get(id=session_id)

        student = Student(
            user=user,
            gender=gender,
            course=course,
            session=session
        )

        student.save()
        messages.success(request, "Student has been saved!")
        return redirect('add_student')

    context = {
        'courses' : courses,
        'sessions' : sessions,
    }
    return render(request, 'hod/add-student.html', context)


def student_list(request):
    students = Student.objects.all()

    context = {
        'students':students,
    }
    return render(request, 'hod/student-list.html', context)


def student_details(request, id):
    student = Student.objects.get(id=id)
    context = {
        'student':student,
    }
    return render(request, 'hod/student-details.html', context)


def update_student(request, id):
    student = get_object_or_404(Student, id=id)
    student_user = student.user

    if request.method == 'POST':
        # Update the studentUser fields
        student_user.first_name = request.POST.get('first_name', student_user.first_name)
        student_user.last_name = request.POST.get('last_name', student_user.last_name)
        date_of_birth = request.POST.get('date_of_birth', student_user.date_of_birth)
        parsed_date = parse_date(date_of_birth)
        if parsed_date:
            student_user.date_of_birth = parsed_date
        student_user.email = request.POST.get('email', student_user.email)
        student_user.mobile = request.POST.get('mobile', student_user.mobile)

        student_user.photo = request.FILe

        student_user.address = request.POST.get('address', student_user.address)
        student_user.save()

        # Update the Student fields
        course_id = request.POST.get('course_id')
        session_id = request.POST.get('session_id')
        try:
            if course_id:
                student.course = Course.objects.get(id=course_id)
            if session_id:
                student.session = Session.objects.get(id=session_id)
        except Course.DoesNotExist:
            messages.error(request, "Selected course does not exist.")
        except Session.DoesNotExist:
            messages.error(request, "Selected session does not exist.")
        student.gender = request.POST.get('gender', student.gender)
        student.save()

        messages.success(request, "Student has been updated!")
        return redirect('student_list')

    #For get requests, load the student data into the form
    courses = Course.objects.all()
    sessions = Session.objects.all()

    context = {
        'student': student,
        'student_user': student_user,
        'courses': courses,
        'sessions': sessions,
    }
    return render(request, 'hod/update-student.html', context)
