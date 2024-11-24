from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser


class CustomUserAdmin(UserAdmin):
    # Add the new fields to list_display
    list_display = ['username', 'email', 'user_type', 'photo']

    # Ensure the new fields appear in the add/edit forms
    fieldsets = UserAdmin.fieldsets + (
        ('Custom Fields', {
            'fields': ('user_type', 'photo'),
        }),
    )

    # For the form used to create a new user
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Custom Fields', {
            'fields': ('user_type', 'photo'),
        }),
    )


# Register the CustomUser with the updated admin class
admin.site.register(CustomUser, CustomUserAdmin)
