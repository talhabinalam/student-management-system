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
    path('hod/subject/add/', hod_views.add_subject, name='add_subject'),
    path('hod/subject/list/', hod_views.subject_list, name='subject_list'),
    path('hod/subject/update/<int:id>/', hod_views.update_subject, name='update_subject'),
    path('hod/subject/delete/<int:id>/', hod_views.delete_subject, name='delete_subject'),
    path('hod/session/add/', hod_views.add_session, name='add_session'),
    path('hod/session/list/', hod_views.session_list, name='session_list'),
    path('hod/session/update/<int:id>/', hod_views.update_session, name='update_session'),
    path('hod/session/delete/<int:id>/', hod_views.delete_session, name='delete_session'),
    path('hod/staff/send_notification/', hod_views.send_staff_notification, name='send_staff_notification'),
    path('hod/staff/save_notification/', hod_views.save_staff_notification, name='save_staff_notification'),
    path('hod/student/send_notification/', hod_views.send_student_notification, name='send_student_notification'),
    path('hod/student/save_notification/', hod_views.save_student_notification, name='save_student_notification'),
    path('hod/staff/view_leave/', hod_views.staff_leave, name='staff_leave'),
    path('hod/staff/leave/approve/<int:id>/', hod_views.staff_approve_leave, name='staff_approve_leave'),
    path('hod/staff/leave/decline/<int:id>/', hod_views.staff_decline_leave, name='staff_decline_leave'),
    path('hod/staff/feedback/replay/', hod_views.staff_feedback_replay, name='staff_feedback_replay'),
    path('hod/student/leave/', hod_views.student_leave, name='student_leave'),
    path('hod/student/leave/approve/<int:id>/', hod_views.student_approve_leave, name='student_approve_leave'),
    path('hod/student/leave/decline/<int:id>/', hod_views.student_decline_leave, name='student_decline_leave'),
    path('hod/student/feedback/replay/', hod_views.student_feedback_replay, name='student_feedback_replay'),
    path('hod/view_attendance', hod_views.hod_view_attendance, name='hod_view_attendance'),


    # staff
    path('staff/home/', staff_views.home, name='staff_home'),
    path('staff/notification/', staff_views.staff_notification, name='staff_notification'),
    path('staff/notification/status/<int:id>/', staff_views.staff_notification_status, name='staff_notification_status'),
    path('staff/apply_leave/', staff_views.apply_staff_leave, name='apply_staff_leave'),
    path('staff/feedback/', staff_views.staff_feedback, name='staff_feedback'),
    path('staff/take_attendance/', staff_views.staff_take_attendance, name='staff_take_attendance'),
    path('staff/save_attendance/', staff_views.staff_save_attendance, name='staff_save_attendance'),
    path('staff/view_attendance/', staff_views.staff_view_attendance, name='staff_view_attendance'),
    path('staff/add_result/', staff_views.add_result, name='add_result'),


    # student
    path('student/home/', student_views.home, name='student_home'),
    path('student/notification/', student_views.student_notification, name='student_notification'),
    path('student/notification/save/<int:id>/', student_views.student_notification_status, name='student_notification_status'),
    path('student/apply_leave/', student_views.apply_student_leave, name='apply_student_leave'),
    path('student/feedback/', student_views.student_feedback, name='student_feedback'),
    path('student/view_attendance/', student_views.student_view_attendance, name='student_view_attendance'),


    path('profile/', views.profile, name='profile'),
    path('update_profile/', views.update_profile, name='update_profile'),
    path('change-password/', views.change_password, name='change_password'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

