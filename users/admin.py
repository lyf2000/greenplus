import os

from django.contrib import admin
from django.contrib.auth import admin as auth_admin
from django.utils.safestring import mark_safe

from .forms import SignupForm
from .models import User


@admin.register(User)
class UserAdmin(auth_admin.UserAdmin):
    # add_form = SignupForm
    add_form_template = 'users/signup.html'
    fieldsets = (
        (None, {'fields': ('username', 'email', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name',)}),
        ('Image info', {
            'fields': ('avatar', 'avatar_image',
                       ),
        }),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser',
                                       'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    limited_fieldsets = (
        (None, {'fields': ('username',)}),
        ('Personal info', {'fields': ('first_name', 'last_name',)}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2')}
        ),
    )
    # form = UserChangeForm
    # add_form = UserCreationForms
    # change_password_form = auth_admin.AdminPasswordChangeForm
    list_display = ('email', 'first_name', 'last_name', 'is_superuser')
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'groups')
    search_fields = ('first_name', 'last_name', 'email')
    ordering = ('email',)
    readonly_fields = ('last_login', 'date_joined', 'avatar_image')

    def avatar_image(self, obj):
        return mark_safe(
            '<img src="{url}" width="{width}" height={height} />'
                .format(
                url=os.path.join('media/', obj.avatar.url),
                # width=obj.avatar.width,
                # height=obj.avatar.height,
                height=550,
                width=800,
            ))

    pass