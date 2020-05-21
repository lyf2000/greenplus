from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Row, Column, Submit, Div, HTML
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.utils.translation import ugettext_lazy as _
from django import forms
from django.contrib.auth import password_validation
from django.contrib.auth.forms import UserCreationForm, PasswordResetForm, SetPasswordForm as setPasswordForm, \
    AuthenticationForm, UserChangeForm as userChangeForm

from users.models import User

# class UserCreationForm(forms.ModelForm):
#     error_messages = {
#         'password_mismatch': "The two password fields didn't match.",
#     }
#     password1 = forms.CharField(label="Password", widget=forms.PasswordInput)
#     password2 = forms.CharField(label="Password confirmation", widget=forms.PasswordInput,
#                                 help_text="Enter the same password as above, for verification.")
#
#     class Meta:
#         model = User
#         fields = ('username', 'email', )
#
#     def clean_password2(self):
#         password1 = self.cleaned_data.get("password1")
#         password2 = self.cleaned_data.get("password2")
#         if password1 and password2 and password1 != password2:
#             raise forms.ValidationError(
#                 self.error_messages['password_mismatch'],
#                 code='password_mismatch',
#             )
#         return password2
#
#     def save(self, commit=True):
#         user = super(UserCreationForm, self).save(commit=False)
#         user.set_password(self.cleaned_data["password1"])
#         if commit:
#             user.save()
#         return user
#
#
# class UserChangeForm(forms.ModelForm):
#     password = auth_forms.ReadOnlyPasswordHashField(label="Password",
#         help_text="Raw passwords are not stored, so there is no way to see "
#                   "this user's password, but you can change the password "
#                   "using <a href=\"password/\">this form</a>.")
#
#     class Meta:
#         model = User
#         fields = '__all__'
#
#     def __init__(self, *args, **kwargs):
#         super(UserChangeForm, self).__init__(*args, **kwargs)
#         f = self.fields.get('user_permissions', None)
#         if f is not None:
#             f.queryset = f.queryset.select_related('content_type')
#
#     def clean_password(self):
#         return self.initial["password"]
from users.tasks import send_reset_email


class SignupForm(UserCreationForm):
    avatar = forms.FileField(required=False, label=_('Avatar'), help_text=_('Avatar image'))
    email = forms.CharField(widget=forms.EmailInput(attrs={'placeholder': 'Email'}))
    password1 = forms.CharField(
        # label=_("Password"),
        strip=False,
        widget=forms.PasswordInput(attrs={'placeholder': 'Password'}),
        # help_text=password_validation.password_validators_help_text_html(),
    )
    password2 = forms.CharField(
        # label=_("Password confirmation"),
        widget=forms.PasswordInput(attrs={'placeholder': 'Password confirmation'}),
        strip=False,
        help_text=_("Enter the same password as before, for verification."),
    )

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2', 'avatar')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_show_labels = True
        self.helper.layout = Layout(
            Row(
                Column('username', css_class='form-group col-md-5 mb-0'),
                Column('email', css_class='form-group col-md-5 mb-0'),
                Column('avatar', css_class='form-group col-md-2 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column('password1', css_class='form-group col-md-6 mb-0'),
                Column('password2', css_class='form-group col-md-6 mb-0'),
                css_class='form-row'
            ),
            # Row(
            #     Column('password2', css_class='form-group col-md-6 mb-0'),
            #     css_class='form-row'
            # ),
            Submit('submit', 'Create')
        )


class PasswordRestForm(PasswordResetForm):
    email = forms.CharField(
        widget=forms.EmailInput(attrs={'placeholder': 'Email'}),
        help_text=_("Enter email"), )

    def __init__(self, *args, **kw):
        super().__init__(*args, **kw)

        self.helper = FormHelper()
        self.helper.form_show_labels = False
        # self.helper.form_class = 'form-horizontal'
        # self.helper.label_class = 'col-lg-2'
        # self.helper.field_class = 'col-lg-6'
        self.helper.layout = Layout(
            Row(
                Column('email', css_class='form-group col-md-3 mb-0'),
                css_class='form-row'
            ),
            Submit('submit', 'Reset password'),
        )

    def save(self, domain_override=None,
             subject_template_name='registration/password_reset_subject.txt',
             email_template_name='users/password_reset_email.html',
             use_https=False, token_generator=default_token_generator,
             from_email=None, request=None, html_email_template_name=None,
             extra_email_context=None):
        """
        Generate a one-use only link for resetting password and send it to the
        user.
        """
        # TODO expired ??
        to_email = self.cleaned_data["email"]

        if not domain_override:
            current_site = get_current_site(request)
            site_name = current_site.name
            domain = current_site.domain
        else:
            site_name = domain = domain_override

        send_reset_email.apply_async(args=(
            to_email, domain, site_name, use_https, subject_template_name, email_template_name, from_email,
            html_email_template_name))
        # for user in users:
        #
        #     context = {
        #         'email': to_email,
        #         'domain': domain,
        #         'site_name': site_name,
        #         'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        #         'user': user.username,
        #         'token': token_generator.make_token(user),
        #         'protocol': 'https' if use_https else 'http',
        #         **(extra_email_context or {}),
        #     }
        #     self.send_mail(
        #         subject_template_name, email_template_name, context, from_email,
        #         to_email, html_email_template_name=html_email_template_name,
        #     )


class SetPasswordForm(setPasswordForm):
    new_password1 = forms.CharField(
        label=_("New password"),
        widget=forms.PasswordInput(
            attrs={'placeholder': 'New password'}
        ),
        strip=False,
        # help_text=password_validation.password_validators_help_text_html(),
    )
    new_password2 = forms.CharField(
        label=_("New password confirmation"),
        strip=False,
        widget=forms.PasswordInput,
    )

    def __init__(self, *args, **kw):
        super().__init__(*args, **kw)

        self.helper = FormHelper()
        # self.helper.form_show_labels = False
        self.helper.layout = Layout(
            Row(
                Column('new_password1', css_class='form-group col-md-3 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column('new_password2', css_class='form-group col-md-3 mb-0'),
                css_class='form-row'
            ),
            Submit('submit', 'Set new password'),
        )


class SignInForm(AuthenticationForm):
    # email = forms.CharField(widget=forms.EmailInput(attrs={'placeholder': 'Email'}))
    # password1 = forms.CharField(
    #     # label=_("Password"),
    #     strip=False,
    #     widget=forms.PasswordInput(attrs={'placeholder': 'Password'}),
    #     # help_text=password_validation.password_validators_help_text_html(),
    # )
    # password2 = forms.CharField(
    #     # label=_("Password confirmation"),
    #     widget=forms.PasswordInput(attrs={'placeholder': 'Password confirmation'}),
    #     strip=False,
    #     help_text=_("Enter the same password as before, for verification."),
    # )
    #
    # class Meta:
    #     model = User
    #     fields = ('username', 'email', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_show_labels = True
        self.helper.layout = Layout(
            Row(
                Column('username', css_class='form-group col-md-6 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column('password', css_class='form-group col-md-6 mb-0'),
                css_class='form-row'
            ),
            # Row(
            #     Column('password2', css_class='form-group col-md-6 mb-0'),
            #     css_class='form-row'
            # ),
            Submit('submit', 'Create')
        )

# class UserChangeForm(userChangeForm):
