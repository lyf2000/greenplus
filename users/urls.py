from django.contrib import admin
from django.contrib.auth.views import LogoutView
from django.urls import path, re_path
from users.views import signup, activate, Reset, PasswordResetConfirmView, PasswordResetDoneView, \
    PasswordResetCompleteView, SignInnView

app_name = 'users'

urlpatterns = [
    re_path(r'^signup/$', signup, name='signup'),
    re_path(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
            activate, name='activate'),
    path('login/', SignInnView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(template_name='users/logged_out.html'), name='logout'),
    path('reset/', Reset.as_view(), name='reset'),
    path('reset/<uidb64>/<token>/', PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/complete/', PasswordResetCompleteView.as_view(), name='password_reset_complete'),
]
