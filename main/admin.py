from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.safestring import mark_safe

from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import *


class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    list_display = ("email", "is_staff", "is_active",)
    list_filter = ("email", "is_staff", "is_active",)
    readonly_fields = ('date', 'get_html_photo')
    fieldsets = (
        (None, {"fields": ("email", "slug", "password", "photo", "get_html_photo", "instagram", "mobile", "date")}),
        ("Permissions", {"fields": ("is_staff", "is_active", "groups", "user_permissions")}),
    )
    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": (
                "email", "password1", "password2", "is_staff",
                "is_active", "groups", "user_permissions"
            )}
        ),
    )
    search_fields = ("email",)
    ordering = ("email",)

    def get_html_photo(self, object):
        if object.photo:
            return mark_safe(f"<img src='{ object.photo.url }' width=50>")
    get_html_photo.short_description = 'Миниатюра'


admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Manicure)
admin.site.register(Service)


admin.site.site_title = 'Маникюр'
admin.site.site_header = 'Маникюр'
admin.site.index_title = 'Админ'
