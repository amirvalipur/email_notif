from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import *
from .forms import UserCreationForm, UserChangeForm


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm

    list_display = ['email_address', 'convert_date_time', 'is_active']
    list_filter = ['is_active', 'is_admin']
    search_fields = ['email_address']
    ordering = ['is_active', 'is_admin']
    list_editable = ['is_active']
    filter_horizontal = ('groups',)

    fieldsets = (
        (None, {'fields': ('email_address', 'password')}),
        ('personal_info', {'fields': ('name', 'family')}),
        ('permissions', {'fields': ('is_active', 'is_admin', 'is_superuser')}),
        ('groups', {'fields': ('groups',)}),
    )

    add_fieldsets = (
        (None, {'fields': ('email_address', 'password1', 'password2')}),
        ('personal info', {'fields': ('name', 'family')}),
    )

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        is_superuser = request.user.is_superuser

        if not is_superuser:
            form.base_fields['is_superuser'].disabled = True
            form.base_fields['is_admin'].disabled = True
            form.base_fields['is_active'].disabled = True
            form.base_fields['groups'].disabled = True
        return form


# _______________________________________________________________
@admin.register(UserEmail)
class UserEmailAdmin(admin.ModelAdmin):
    list_display = ['user', 'email', 'convert_date_time']
    list_filter = ['user', 'email', 'send_datetime']


# _______________________________________________________________
@admin.register(Email)
class EmailAdmin(admin.ModelAdmin):
    list_display = ['subject', 'slug']
    list_filter = ['subject']
