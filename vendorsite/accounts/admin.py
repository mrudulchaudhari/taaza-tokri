from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

class CustomUserAdmin(UserAdmin):
    # The model we are using
    model = CustomUser
    
    # Fields to display in the list view of users
    # CORRECTED: 'username' is removed and replaced with other useful fields.
    list_display = ('email', 'first_name', 'last_name', 'user_type', 'is_staff')
    
    # How the admin list should be sorted
    # CORRECTED: Sort by 'email' since 'username' is gone. This fixes the error.
    ordering = ('email',)

    # The fields to show when editing a user
    # This is required to remove 'username' from the edit view.
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'user_type')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    
    # Fields to show when adding a user
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'first_name', 'last_name', 'user_type', 'password', 'password2'),
        }),
    )
    
    # Fields to use for searching
    search_fields = ('email', 'first_name', 'last_name')


# Register your CustomUser model with the corrected admin class
admin.site.register(CustomUser, CustomUserAdmin)
