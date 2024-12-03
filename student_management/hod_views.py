from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from app.models import *


def home(request):
    return render(request, 'hod/home.html')


def add_student(request):
    course = Course.objects.all()
    session = Session.objects.all()

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
        course_id = request.POST.get('course')
        session_id = request.POST.get('session')

        if CustomUser.objects.filter(email=email).exists():
            messages.warning(request, "Email already exists!")
            return redirect('add_student')

        if password != confirm_password:
            messages.error(request, "Password did not match!")
            return redirect('add_student')

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
        'courses' : course,
        'sessions' : session,
    }
    return render(request, 'hod/add-student.html', context)



def student_list(request):
    students = Student.objects.all()

    context = {
        'students':students,
    }
    return render(request, 'hod/view-student.html', context)



def student_details(request, id):
    student = Student.objects.get(id=id)
    context = {
        'student':student,
    }
    return render(request, 'hod/student-details.html', context)