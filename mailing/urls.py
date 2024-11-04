from django.urls import path

from config.urls import urlpatterns
from mailing.apps import MailingConfig

app_name =MailingConfig.name

urlpatterns = [
    path('', ),
    path('', ),
    path('', ),

]