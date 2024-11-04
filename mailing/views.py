from django.views.generic import ListView

from django.shortcuts import render

from mailing.models import Recipient


# Create your views here.
class RecipientListView(ListView):
    model = Recipient
    template_name = 'mailing/recipient_list.html'
    context_object_name = 'recipient'
    paginate_by = 10
