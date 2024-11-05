from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from pyexpat.errors import messages

from mailing.forms import RecipientForm, MessageForm
from mailing.models import Recipient, Message


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
    template_name = 'mailing/confirm_delete.html'
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
