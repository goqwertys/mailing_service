from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path, reverse_lazy
from django.contrib.auth import views as auth_views
from users.apps import UsersConfig
from users.views import UserCreationView, email_verification, UserProfileUpdateView

app_name = UsersConfig.name

urlpatterns = [
    path('login/', LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', LogoutView.as_view(next_page='/mailing/recipients'), name='logout'),
    path('register/', UserCreationView.as_view(), name='register'),
    path('email-confirm/<str:token>/', email_verification, name='email_confirm'),
    path('profile/edit/', UserProfileUpdateView.as_view(), name='profile_edit'),

    # PASSWORD RESET FEATURE
    path(
        'password_reset/',
        auth_views.PasswordResetView.as_view(
            template_name='users/password_reset.html',
            email_template_name='users/password_reset_email.html',
            subject_template_name='users/password_reset_subject.txt',
            success_url=reverse_lazy('users:password_reset_done')
        ),
        name='password_reset'),
    path(
        'password_reset/done/',
        auth_views.PasswordResetDoneView.as_view(
            template_name='users/password_reset_done.html'
        ),
        name='password_reset_done'),
    path(
        'password_reset/confirm/<uidb64>/<token>/',
        auth_views.PasswordResetConfirmView.as_view(
            template_name='users/password_reset_confirm.html',
            success_url=reverse_lazy('users:password_reset_complete')
        ),
        name='password_reset_confirm'
    ),
    path(
        'password_reset/complete/',
        auth_views.PasswordResetCompleteView.as_view(
            template_name='users/password_reset_complete.html'
        ),
        name='password_reset_complete'
    )
]
