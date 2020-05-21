from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.mixins import UserPassesTestMixin, AccessMixin
from django.contrib.auth.views import PasswordResetView, PasswordResetConfirmView as passwordResetConfirmView, \
    PasswordResetDoneView as passwordResetDoneView, PasswordResetCompleteView as passwordResetCompleteView, \
    LoginView as loginView
from django.contrib.sites.shortcuts import get_current_site
from django.shortcuts import render, redirect
# Create your views here.
from django.urls import reverse_lazy, reverse
from django.utils.encoding import force_text
from django.utils.http import urlsafe_base64_decode

from users.forms import SignupForm, PasswordRestForm, SetPasswordForm, SignInForm, UserChangeForm
from users.models import User
from users.tasks import send_register_confirmation_email
from users.tokens import account_activation_token


@user_passes_test(lambda user: user.is_anonymous,
                  login_url=reverse_lazy('already-logined'),
                  redirect_field_name=None)
def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()

            current_site = get_current_site(request)
            domain = current_site.domain
            to_email = form.cleaned_data.get('email')
            send_register_confirmation_email.delay(user.pk, domain, to_email)

            return render(request, 'users/signup_confirm_sent.html')
    else:
        form = SignupForm()
    return render(request, 'users/signup.html', {'form': form})


@user_passes_test(lambda user: user.is_anonymous,
                  login_url=reverse_lazy('already-logined'),
                  redirect_field_name=None)
def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        # return redirect('home')
        return render(request, 'users/signup_activated.html')
    else:
        return render(request, 'users/signup_activated_fail.html')


@login_required(login_url=reverse_lazy('home'))
def already_logined(request):
    return render(request, 'already_logined.html')


class AnonymousRequiredMixin(AccessMixin):
    """Verify that the current user is authenticated."""

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return self.handle_no_permission()
        return super().dispatch(request, *args, **kwargs)

    def handle_no_permission(self):
        return redirect(reverse('already-logined'))


class SignInnView(AnonymousRequiredMixin, loginView):
    form_class = SignInForm
    template_name = 'users/login.html'
    redirect_authenticated_user = True
#     TODO next (REDIRECT_FIELD_NAME)


class Reset(PasswordResetView):
    form_class = PasswordRestForm
    template_name = 'users/password_reset.html'
    html_email_template_name = 'users/password_reset_email.html'
    email_template_name = 'users/password_reset_email.html'
    success_url = reverse_lazy('users:password_reset_done')


class PasswordResetConfirmView(passwordResetConfirmView):
    form_class = SetPasswordForm
    template_name = 'users/password_reset_confirm.html'
    success_url = reverse_lazy('users:password_reset_complete')


class PasswordResetDoneView(passwordResetDoneView):
    template_name = 'users/password_reset_done.html'


class PasswordResetCompleteView(passwordResetCompleteView):
    template_name = 'users/password_reset_complete.html'


def change_user(request):
    if request.method == 'POST':
        user = UserChangeForm(request.POST, request.FILES, instance=request.user)
        if user.is_valid():
            user.save()
            # redirect(reverse())
        else:
            return render(request, 'users/user-change.html', {'form': user})
    user = request.user
    form = UserChangeForm(initial={
        'username': user.username,
        'email': user.email
    })
    return render(request, 'users/user-change.html', {'form': form})
