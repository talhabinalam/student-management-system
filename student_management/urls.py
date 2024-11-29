
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
    path('hod/home/', hod_views.home, name='hod-home'),

    # staff
    # path('staff/home/', staff_views.home, name='staff-home'),

    # student
#     path('student/home/', student_views.home, name='student-home'),

    path('profile/', views.profile, name='profile'),
    path('update_profile/', views.update_profile, name='update_profile'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
