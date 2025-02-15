from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User

class CustomUserAdmin(UserAdmin):
    model = User
    list_display = ['email', 'username', 'is_staff', 'is_verified', 'created_at'] # Defines which fields appear in the table view of users
    list_filter = ['is_staff', 'is_verified'] # Adds a filter sidebar to the user list page, allowing you to filter users by staff status and verification status.
    fieldsets = ( # This organizes how user details are displayed when editing an existing user, grouped into three sections:
        (None, {'fields': ('email', 'username', 'password')}),
        ('Permissions', {'fields': ('is_staff', 'is_active', 'is_verified')}),
        ('Important dates', {'fields': ('last_login', 'created_at', 'updated_at')}),
    )
    add_fieldsets = ( # This defines which fields appear when creating a new user in the admin interface.
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'username', 'password1', 'password2', 'is_staff', 'is_active', 'is_verified')
        }),
    )
    search_fields = ['email', 'username']
    ordering = ['email']

admin.site.register(User, CustomUserAdmin)