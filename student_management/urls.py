
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from student_management import student_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('base/', student_views.base,),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
