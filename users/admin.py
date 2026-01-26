from django.contrib import admin
from users.models import CustomUserModel
from django.contrib.auth.admin import UserAdmin

@admin.register(CustomUserModel)
class CustomUserAdmin(UserAdmin):
    list_display = 'id username phone_num is_active'.split()
    ordering = 'phone_num'.split()
    fieldsets = (
        (None, {"fields": ('username' ,"phone_num", "password")}), 
        (
            ("Permissions"),
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                ),
            },
        ),
        (("Important dates"), {"fields": ("last_login",)}),
    )