from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin, UserPassesTestMixin
from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView
from django.contrib import messages

from mailing.forms import RecipientForm, MessageForm, MailingForm
from mailing.models import Recipient, Message, Mailing, Attempt
from mailing.services import get_recipients_from_cache, get_mailings_from_cache, get_messages_from_cache
from mailing.utils import send_mailing


# Recipient CRUD
class RecipientListView(ListView):
    model = Recipient
    template_name = 'mailing/recipient_list.html'
    context_object_name = 'recipients'
    paginate_by = 10

    def get_queryset(self):
        if self.request.user.is_superuser or self.request.user.has_perm('mailing.can_view_other_recipient'):
            return get_recipients_from_cache()
        return Recipient.objects.filter(user=self.request.user)


class RecipientDetailView(LoginRequiredMixin, DetailView):
    model = Recipient
    template_name = 'mailing/recipient_detail.html'
    context_object_name = 'recipient'

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        if not self.request.user.is_superuser and not self.request.user.has_perm('mailing.can_view_other_recipient') and obj.user != self.request.user:
            raise PermissionDenied('You do not have permission to view this recipient.')
        return obj


class RecipientCreateView(LoginRequiredMixin, CreateView):
    model = Recipient
    form_class = RecipientForm
    template_name = 'mailing/recipient_form.html'
    success_url = reverse_lazy('mailing:recipients')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class RecipientUpdateView(LoginRequiredMixin, UpdateView):
    model = Recipient
    form_class = RecipientForm
    template_name = 'mailing/recipient_form.html'
    success_url = reverse_lazy('mailing:recipients')

    def get_queryset(self):
        return Recipient.objects.filter(user=self.request.user)

    def get_object(self, queryset=None):
        try:
            return super().get_object(queryset)
        except Recipient.DoesNotExist:
            raise PermissionDenied('You do not have permission to edit this recipient.')


class RecipientDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Recipient
    template_name = 'mailing/recipient_confirm_delete.html'
    success_url = reverse_lazy('mailing:recipients')

    def test_func(self):
        obj = self.get_object()
        return self.request.user.has_perm('mailing.recipient_delete') or obj.user == self.request.user

    def handle_no_permission(self):
        return redirect('mailing:recipient_list')


# Messages CRUD
class MessageListView(ListView):
    model = Message
    template_name = 'mailing/message_list.html'
    context_object_name = 'messages'
    paginate_by = 10

    def get_queryset(self):
        if self.request.user.is_superuser or self.request.user.has_perm('mailing.can_view_other_message'):
            return get_messages_from_cache()
        return Message.objects.filter(user=self.request.user)


class MessageDetailView(LoginRequiredMixin, DetailView):
    model = Message
    template_name = 'mailing/message_detail.html'
    context_object_name = 'message'

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        if not self.request.user.is_superuser and not self.request.user.has_perm('mailing.can_view_other_message') and obj.user != self.request.user:
            raise PermissionDenied('You do not have permission to view this message.')
        return obj


class MessageCreateView(LoginRequiredMixin, CreateView):
    model = Message
    form_class = MessageForm
    template_name = 'mailing/message_form.html'
    success_url = reverse_lazy('mailing:messages')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class MessageUpdateView(LoginRequiredMixin, UpdateView):
    model = Message
    form_class = MessageForm
    template_name = 'mailing/message_form.html'
    success_url = reverse_lazy('mailing:messages')

    def get_queryset(self):
        return Message.objects.filter(user=self.request.user)

    def get_object(self, queryset=None):
        try:
            return super().get_object(queryset)
        except Message.DoesNotExist:
            raise PermissionDenied('You do not have permission to edit this message.')


class MessageDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Message
    template_name = 'mailing/message_confirm_delete.html'
    success_url = reverse_lazy('mailing:messages')

    def test_func(self):
        obj = self.get_object()
        return self.request.user.has_perm('mailing.message_delete') or obj.user == self.request.user


# Mailing CRUD
class MailingListView(ListView):
    model = Mailing
    template_name = 'mailing/mailing_list.html'
    context_object_name = 'mailings'
    paginate_by = 10

    def get_queryset(self):
        if self.request.user.is_superuser or self.request.user.has_perm('mailing.can_view_other_mailing'):
            return get_mailings_from_cache()
        return Mailing.objects.filter(user=self.request.user)


class MailingDetailView(LoginRequiredMixin, DetailView):
    model = Mailing
    template_name = 'mailing/mailing_detail.html'
    context_object_name = 'mailing'

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        if not self.request.user.is_superuser and not self.request.user.has_perm('mailing.can_view_other_mailing') and obj.user != self.request.user:
            raise PermissionDenied('You do not have permission to view this mailing.')
        return obj


class MailingCreateView(LoginRequiredMixin, CreateView):
    model = Mailing
    form_class = MailingForm
    template_name = 'mailing/mailing_form.html'
    success_url = reverse_lazy('mailing:mailings')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        mailing = form.save(commit=False)
        mailing.user = self.request.user
        mailing.save()
        form.save_m2m()
        return super().form_valid(form)


class MailingUpdateView(LoginRequiredMixin, UpdateView):
    model = Mailing
    form_class = MailingForm
    template_name = 'mailing/mailing_form.html'
    success_url = reverse_lazy('mailing:mailings')

    def get_queryset(self):
        return Mailing.objects.filter(user=self.request.user)

    def get_object(self, queryset=None):
        try:
            return super().get_object(queryset)
        except Mailing.DoesNotExist:
            raise PermissionDenied('You do not have permission to edit this mailing.')


class MailingDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Mailing
    template_name = 'mailing/mailing_confirm_delete.html'
    success_url = reverse_lazy('mailing:mailings')

    def test_func(self):
        obj = self.get_object()
        return self.request.user.has_perm('mailing.mailing_delete') or obj.user == self.request.user

    def handle_no_permission(self):
        return redirect('mailing:mailing_list')

    def get_object(self, queryset=None):
        return get_object_or_404(Mailing, pk=self.kwargs.get('pk'))


# Attempt CRUD
class AttemptListView(ListView):
    model = Attempt
    template_name = 'mailing/attempt_list_view.html'
    context_object_name = 'attempts'
    paginate_by = 10

    def get_queryset(self):
        return Attempt.objects.filter(mailing__user=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        queryset = self.get_queryset()
        context["attempts_count"] = queryset.count()
        context["attempts_success_count"] = queryset.filter(status="CM").count()
        return context


class AttemptDetailView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    model = Attempt
    template_name = 'mailing/attempt_detail.html'
    context_object_name = 'attempt'

    def test_func(self):
        obj = self.get_object()
        return self.request.user.has_perm('mailing.view_attempt') or obj.mailing.user == self.request.user

    def get_queryset(self):
        return Attempt.objects.filter(mailing__user=self.request.user)


# Start_mailing
@login_required
@permission_required('mailing.start_mailing', raise_exception=True)
def start_mailing(request, mailing_id):
    mailing = get_object_or_404(Mailing, id=mailing_id, user=request.user)
    try:
        send_mailing(mailing.id, request.user)
        messages.success(request, 'Mailing has been sent.')
    except ValueError as e:
        messages.error(request, str(e))
    return redirect('mailing:mailings')


# Home view
class HomeView(TemplateView):
    template_name = 'mailing/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['all_mailings_count'] = Mailing.objects.count()
        context['successful_attempts'] = Attempt.objects.filter(status='CM').count()
        context['unsuccessful_attempts'] = Attempt.objects.filter(status='FLpy').count()
        context['unique_recipients'] = Recipient.objects.values('email').distinct().count()
        return context
