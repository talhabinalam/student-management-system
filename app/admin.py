from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import *

class CustomUserAdmin(UserAdmin):
    model = CustomUser

    # Customize the order of fields
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal Info', {'fields': ('first_name', 'last_name', 'date_of_birth', 'mobile', 'address')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important Dates', {'fields': ('last_login', 'date_joined')}),
        ('Custom Fields', {'fields': ('user_type', 'photo')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'first_name', 'last_name', 'password1', 'password2', 'user_type'),
        }),
    )

    list_display = ('email', 'first_name', 'last_name', 'user_type', 'is_staff')
    search_fields = ('email', 'user_type')
    ordering = ('email',)
    readonly_fields = ('last_login', 'date_joined')


class CourseAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at', 'updated_at', )
    readonly_fields = ('created_at', 'updated_at')


class StudentAdmin(admin.ModelAdmin):
    list_display = ('user', 'gender', 'course', 'session', 'created_at', 'updated_at')
    readonly_fields = ('created_at', 'updated_at')


# Register the customized admin class
admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Course, CourseAdmin)
admin.site.register(Session)
admin.site.register(Student, StudentAdmin)