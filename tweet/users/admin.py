from django.contrib import admin

from django.contrib.auth.admin import UserAdmin

from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import CustomUser


class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    list_display = ("email", "user_name", "date_joined", "date_of_birth", "is_staff", "is_active",)
    list_filter = ("date_joined", "date_of_birth","is_staff", "is_active",)
    fieldsets = (
        (None, {"fields": ("email", "password")}),
        ("Permissions", {"fields": ("is_staff", "is_active", "groups", "user_permissions")}),
    )
    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": (
                "email", "user_name", "date_of_birth", "password1", "password2", "is_staff",
                "is_active", "groups", "user_permissions"
            )}
        ),
    )
    search_fields = ("email", "user_name", "date_of_birth", "date_joined",)
    ordering = ("email", "user_name", "date_of_birth", "date_joined",)


admin.site.register(CustomUser, CustomUserAdmin)