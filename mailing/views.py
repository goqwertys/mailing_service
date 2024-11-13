from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView
from pyexpat.errors import messages

from mailing.forms import RecipientForm, MessageForm, MailingForm
from mailing.models import Recipient, Message, Mailing, Attempt
from mailing.utils import send_mailing


# Recipient CRUD
class RecipientListView(ListView):
    model = Recipient
    template_name = 'mailing/recipient_list.html'
    context_object_name = 'recipients'
    paginate_by = 10


class RecipientDetailView(DetailView):
    model = Recipient
    template_name = 'mailing/recipient_detail.html'
    context_object_name = 'recipient'


class RecipientCreateView(CreateView):
    model = Recipient
    form_class = RecipientForm
    template_name = 'mailing/recipient_form.html'
    success_url = reverse_lazy('mailing:recipients')


class RecipientUpdateView(UpdateView):
    model = Recipient
    form_class = RecipientForm
    template_name = 'mailing/recipient_form.html'
    success_url = reverse_lazy('mailing:recipients')


class RecipientDeleteView(DeleteView):
    model = Recipient
    template_name = 'mailing/recipient_confirm_delete.html'
    success_url = reverse_lazy('mailing:recipients')

    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Recipient has been deleted successfully')
        return super().delete(request, *args, **kwargs)


# Messages CRUD
class MessageListView(ListView):
    model = Message
    template_name = 'mailing/message_list.html'
    context_object_name = 'messages'
    paginate_by = 10


class MessageDetailView(DetailView):
    model = Message
    template_name = 'mailing/message_detail.html'
    context_object_name = 'message'


class MessageCreateView(CreateView):
    model = Message
    form_class = MessageForm
    template_name = 'mailing/message_form.html'
    success_url = reverse_lazy('mailing:messages')


class MessageUpdateView(UpdateView):
    model = Message
    form_class = MessageForm
    template_name = 'mailing/message_form.html'
    success_url = reverse_lazy('mailing:messages')


class MessageDeleteView(DeleteView):
    model = Message
    template_name = 'mailing/message_confirm_delete.html'
    success_url = reverse_lazy('mailing:messages')

    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Recipient has been deleted successfully')
        return super().delete(request, *args, **kwargs)


# Mailing CRUD
class MailingListView(ListView):
    model = Mailing
    template_name = 'mailing/mailing_list.html'
    context_object_name = 'mailings'
    paginate_by = 10


class MailingDetailView(DetailView):
    model = Mailing
    template_name = 'mailing/mailing_detail.html'
    context_object_name = 'mailing'


class MailingCreateView(CreateView):
    model = Mailing
    form_class = MailingForm
    template_name = 'mailing/mailing_form.html'
    success_url = reverse_lazy('mailing:mailings')


class MailingUpdateView(CreateView):
    model = Mailing
    form_class = MailingForm
    template_name = 'mailing/mailing_form.html'
    success_url = reverse_lazy('mailing:mailings')


class MailingDeleteView(DeleteView):
    model = Mailing
    template_name = 'mailing/mailing_confirm_delete.html'
    success_url = reverse_lazy('mailing:mailings')


# Attempt CRUD
class AttemptListView(ListView):
    model = Attempt
    template_name = 'mailing/attempt_list_view.html'
    context_object_name = 'attempts'
    paginate_by = 10


class AttemptDetailView(DetailView):
    model = Attempt
    template_name = 'mailing/attempt_detail.html'
    context_object_name = 'attempt'


# Start_mailing
def start_mailing(request, mailing_id):
    mailing = get_object_or_404(Mailing, id=mailing_id)
    send_mailing(mailing.id)
    return redirect('mailing:mailings')

# Home view
class HomeView(TemplateView):
    template_name = 'mailing/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data( **kwargs)
        # TODO
        return context
