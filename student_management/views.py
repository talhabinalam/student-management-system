from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth import update_session_auth_hash
from django.contrib import messages


def get_redirect_url(user):
    if user.user_type == 'HOD':
        return 'hod_home'
    elif user.user_type == 'STAFF':
        return 'staff_home'
    elif user.user_type == 'STUDENT':
        return 'student_home'
    else:
        return 'login'  # Fallback for undefined user types


def user_login(request):
    if not request.user.is_authenticated:
        if request.method == 'POST':
            email = request.POST.get('email')
            password = request.POST.get('password')
            user = authenticate(request, username=email, password=password)
            print(user)
            if user is not None:
                login(request, user)
                # return redirect(get_redirect_url(request.user))
                if user.user_type == 'HOD':
                    return redirect('hod_home')
                elif user.user_type == 'STAFF':
                    return redirect('staff_home')
                elif user.user_type == 'STUDENT':
                    return redirect('student_home')
            else:
                messages.error(request, "Invalid email or password!")
                return redirect('login')
        return render(request, 'login.html')
    else:
        return redirect(get_redirect_url(request.user))



def user_logout(request):
    logout(request)
    return redirect('login')



def profile(request):
    return render(request, 'profile.html')



def update_profile(request):
    user = request.user

    if request.method == 'POST':
        # Update the CustomUser fields
        user.first_name = request.POST.get('first_name', user.first_name)
        user.last_name = request.POST.get('last_name', user.last_name)
        user.date_of_birth = request.POST.get('date_of_birth', user.date_of_birth)
        user.mobile = request.POST.get('mobile', user.mobile)
        user.address = request.POST.get('address', user.address)

        #Update photo if new file is uploaded
        if 'photo' in request.FILES:
            user.photo = request.FILES['photo']

        user.save()
        messages.success(request, "Profile has been updated")
        return redirect('profile')

    return render(request, 'update-profile.html')



def change_password(request):
    user = request.user

    if request.method == 'POST':
        password = request.POST.get('password')
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')

        if not user.check_password(password):
            messages.error(request, "Old password is incorrect!")
            return redirect('profile')

        if new_password != confirm_password:
            messages.error(request, "New password did not match!")
            return redirect('profile')

        if password == new_password:
            messages.error(request, "New password must be different!")
            return redirect('profile')

        if len(new_password) < 8:
            messages.error(request, "Password must be at least 8 characters!")
            return redirect('profile')

        user.set_password(new_password)
        user.save()
        update_session_auth_hash(request, user)

        messages.success(request, "Password was successfully updated!")
        return redirect('profile')
    return render(request, 'profile.html')







