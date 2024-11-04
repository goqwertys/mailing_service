from django.urls import path
from mailing.apps import MailingConfig
from mailing.views import RecipientListView, RecipientDetailView, RecipientCreateView, RecipientUpdateView, \
    RecipientDeleteView

app_name = MailingConfig.name

urlpatterns = [
    path('recipients/', RecipientListView.as_view(), name='recipients'),
    path('recipients/<int:pk>/', RecipientDetailView.as_view(), name='recipient_detail'),
    path('recipients/add/', RecipientCreateView.as_view(), name='recipient_create'),
    path('recipients/<int:pk>/edit/', RecipientUpdateView.as_view(), name='recipient_edit'),
    path('recipients/<int:pk>/delete/', RecipientDeleteView.as_view(), name='recipient_delete'),
]
