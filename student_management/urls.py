from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from student_management import views, hod_views, student_views, staff_views

urlpatterns = [
    path('admin/', admin.site.urls),
    # path('base/', student_views.base,),

    path('', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),

    # hod
    path('hod/home/', hod_views.home, name='hod_home'),
    path('hod/student/add/', hod_views.add_student, name='add_student'),
    path('hod/student/list/', hod_views.student_list, name='student_list'),
    path('hod/student/details/<int:id>/', hod_views.student_details, name='student_details'),
    path('hod/student/update/<int:id>/', hod_views.update_student, name='update_student'),
    path('hod/student/delete/<int:id>/', hod_views.delete_student, name='delete_student'),
    path('hod/course/add/', hod_views.add_course, name='add_course'),
    path('hod/course/list/', hod_views.course_list, name='course_list'),
    path('hod/course/delete/<int:id>/', hod_views.delete_course, name='delete_course'),
    path('hod/course/update/<int:id>/', hod_views.update_course, name='update_course'),
    path('hod/staff/add/', hod_views.add_staff, name='add_staff'),
    path('hod/staff/list/', hod_views.staff_list, name='staff_list'),
    path('hod/staff/details/<int:id>/', hod_views.staff_details, name='staff_details'),
    path('hod/staff/update/<int:id>/', hod_views.update_staff, name='update_staff'),
    path('hod/staff/delete/<int:id>/', hod_views.delete_staff, name='delete_staff'),

    # staff
    # path('staff/home/', staff_views.home, name='staff-home'),

    # student
    #path('student/home/', student_views.home, name='student-home'),

    path('profile/', views.profile, name='profile'),
    path('update_profile/', views.update_profile, name='update_profile'),

    path('change-password/', views.change_password, name='change_password'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
