from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path, reverse_lazy
from django.contrib.auth import views as auth_views
from users.apps import UsersConfig
from users.views import UserCreationView, email_verification, UserProfileUpdateView, UserDetailView, \
    block_user, UserListView, unblock_user, \
    ModeratorRecipientListView, ModeratorMailingListView, disable_mailing

app_name = UsersConfig.name

urlpatterns = [
    path('login/', LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', LogoutView.as_view(next_page='/mailing/'), name='logout'),
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
    ),

    # # MODERATOR FEATURES
    path('moderator/users/', UserListView.as_view(), name='moderator_user_list'),
    path('moderator/users/<int:pk>/', UserDetailView.as_view(), name='moderator_user_detail'),
    path('moderator/recipients/', ModeratorRecipientListView.as_view(), name='moderator_recipient_list'),
    path('moderator/mailings/', ModeratorMailingListView.as_view(), name='moderator_mailing_list'),
    path('moderator/users/<int:user_id>/block/', block_user, name='moderator_block_user'),
    path('moderator/users/<int:user_id>/unblock', unblock_user, name='moderator_unblock_user'),
    path('moderator/mailings/<int:mailing_id>/disable', disable_mailing, name='moderator_disable_mailing'),
]
