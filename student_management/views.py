from django.shortcuts import render, redirect
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
            if user is not None:
                login(request, user)
                # Redirect user on different page based on their type
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
        # Update the user fields if provided in the request, else retain current values
        user.first_name = request.POST.get('first_name', user.first_name)
        user.last_name = request.POST.get('last_name', user.last_name)
        user.date_of_birth = request.POST.get('date_of_birth', user.date_of_birth)
        user.mobile = request.POST.get('mobile', user.mobile)
        user.address = request.POST.get('address', user.address)

        # Update profile photo if a new file is uploaded
        if 'photo' in request.FILES:
            user.photo = request.FILES['photo']

        # Save the updated user profile
        user.save()
        messages.success(request, "Profile has been successfully updated!")
        return redirect('profile')

    return render(request, 'update-profile.html')



def change_password(request):
    user = request.user

    if request.method == 'POST':
        # Retrieve form inputs
        current_password = request.POST.get('password')
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')

        # Validate the current password
        if not user.check_password(current_password):
            messages.error(request, "Old password is incorrect!")
            return redirect('profile')

        # Ensure new passwords match
        if new_password != confirm_password:
            messages.error(request, "New passwords do not match!")
            return redirect('profile')

        # Ensure the new password is different from the current password
        if current_password == new_password:
            messages.error(request, "New password must be different from the current password!")
            return redirect('profile')

        # Ensure new password meets length requirement
        if len(new_password) < 8:
            messages.error(request, "Password must be at least 8 characters long!")
            return redirect('profile')

        # Set the new password and keep the user logged in
        user.set_password(new_password)
        user.save()
        update_session_auth_hash(request, user)  # Prevent logout after password change

        messages.success(request, "Your password has been successfully updated!")
        return redirect('profile')

    return render(request, 'profile.html')
