from django.urls import path
from mailing.apps import MailingConfig
from mailing.views import RecipientListView, RecipientDetailView, RecipientCreateView, RecipientUpdateView, \
    RecipientDeleteView, MessageListView, MessageDetailView, MessageCreateView, MessageUpdateView, MessageDeleteView, \
    MailingListView, MailingCreateView, MailingDetailView, MailingUpdateView, MailingDeleteView, start_mailing, \
    AttemptListView, AttemptDetailView, HomeView

app_name = MailingConfig.name

urlpatterns = [
    # Recipients CRUD
    path('recipients/', RecipientListView.as_view(), name='recipients'),
    path('recipients/<int:pk>/', RecipientDetailView.as_view(), name='recipient_detail'),
    path('recipients/add/', RecipientCreateView.as_view(), name='recipient_create'),
    path('recipients/<int:pk>/edit/', RecipientUpdateView.as_view(), name='recipient_edit'),
    path('recipients/<int:pk>/delete/', RecipientDeleteView.as_view(), name='recipient_delete'),

    # Messages CRUD
    path('messages/', MessageListView.as_view(), name='messages'),
    path('messages/<int:pk>/', MessageDetailView.as_view(), name='message_detail'),
    path('messages/add/', MessageCreateView.as_view(), name='message_create'),
    path('messages/<int:pk>/edit', MessageUpdateView.as_view(), name='message_edit'),
    path('messages/<int:pk>/delete', MessageDeleteView.as_view(), name='message_delete'),

    # Mailings CRUD
    path('mailings/', MailingListView.as_view(), name='mailings'),
    path('mailings/<int:pk>/', MailingDetailView.as_view(), name='mailing_detail'),
    path('mailings/create/', MailingCreateView.as_view(), name='mailing_create'),
    path('mailings/<int:pk>/update/', MailingUpdateView.as_view(), name='mailing_update'),
    path('mailings/<int:pk>/delete/', MailingDeleteView.as_view(), name='mailing_delete'),

    # Attempt CRUD
    path('attempts/', AttemptListView.as_view(), name='attempts'),
    path('attempts/<int:pk>/', AttemptDetailView.as_view(), name='attempt_detail'),

    # Mailing
    path('mailing/<int:mailing_id>/start/', start_mailing, name='start_mailing'),

    # Home
    path('', HomeView.as_view(), name='home')
]
