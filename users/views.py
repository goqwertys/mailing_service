import secrets
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, UpdateView, DetailView, ListView

from config.settings import EMAIL_HOST_USER
from mailing.models import Mailing, Recipient, Message, Attempt
from users.forms import UserRegisterForm, UserProfileForm
from users.models import User


class UserCreationView(CreateView):
    model = User
    form_class = UserRegisterForm
    success_url = reverse_lazy('users:login')

    def form_valid(self, form):
        user = form.save(commit=False)
        user.is_active = False

        token = secrets.token_hex(16)
        user.token = token
        user.save()

        host = self.request.get_host()
        url = f'http://{host}/users/email-confirm/{token}'
        send_mail(
            subject='Email confirmation',
            message=f'Follow the link to confirm your registration {url}',
            from_email=EMAIL_HOST_USER,
            recipient_list=[user.email]
        )
        return super().form_valid(form)


def email_verification(request, token):
    user = get_object_or_404(User, token=token)
    user.is_active = True
    user.save()
    return redirect(reverse('users:login'))


class UserProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = User
    form_class = UserProfileForm
    template_name = 'users/profile_edit.html'
    success_url = reverse_lazy('mailing:recipients')

    def get_object(self, queryset=None):
        return self.request.user


# MODERATOR FEATURES
class UserListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = User
    template_name = 'users/moderator_user_list.html'
    context_object_name = 'users'
    permission_required = 'users.view_user'
    paginate_by = 10


class UserDetailView(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    model = User
    template_name = 'users/moderator_user_detail.html'
    context_object_name = 'user'
    permission_required = 'users.view_user'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.object

        context['recipients_count'] = Recipient.objects.filter(user=user).count()
        context['messages_count'] = Message.objects.filter(user=user).count()
        context['mailings_count'] = Mailing.objects.filter(user=user).count()
        context['attempts_count'] = Attempt.objects.filter(user=user).count()

        return context


class ModeratorRecipientListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = Recipient
    template_name = 'users/moderator_recipient_list.html'
    context_object_name = 'recipients'
    permission_required = 'mailing.view_all_recipients'
    paginate_by = 10


class ModeratorMailingListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = Mailing
    template_name = 'users/moderator_mailing_list.html'
    context_object_name = 'mailings'
    permission_required = 'mailing.view_all_mailings'
    paginate_by = 10


@login_required
@permission_required('users.block_user', raise_exception=True)
def block_user(requset, user_id):
    user = get_object_or_404(User, id=user_id)
    user.is_active = False
    user.save()
    return redirect('users:moderator_user_detail', pk=user_id)


@login_required
@permission_required('users.block_user', raise_exception=True)
def unblock_user(requset, user_id):
    user = get_object_or_404(User, id=user_id)
    user.is_active = True
    user.save()
    return redirect('users:moderator_user_detail', pk=user_id)


@login_required
@permission_required('mailing.disable_mailing', raise_exception=True)
def disable_mailing(request, mailing_id):
    mailing = get_object_or_404(Mailing, id=mailing_id)
    mailing.status = 'DSBL'
    mailing.save()
    return redirect('users:moderator_mailing_list')
