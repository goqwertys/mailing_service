from django.core.cache import cache

from config.settings import CACHE_ENABLED
from mailing.models import Mailing, Recipient, Message


def get_recipients_from_cache():
    """ Gets recipients from cache """
    if not CACHE_ENABLED:
        return Recipient.objects.all()
    key = 'recipient_key'
    recipients = cache.get(key)
    if recipients:
        return recipients
    recipients = Recipient.objects.all()
    cache.set(key, recipients)
    return recipients


def get_messages_from_cache():
    """ Gets messages from cache """
    if not CACHE_ENABLED:
        return Message.objects.all()
    key = 'messages_key'
    messages = cache.get(key)
    if messages:
        return messages
    messages = Message.objects.all()
    cache.set(key, messages)
    return messages


def get_mailings_from_cache():
    """ Gets mailing data from cache """
    if not CACHE_ENABLED:
        return Mailing.objects.all()
    key = 'mailing_list'
    mailings = cache.get(key)
    if mailings:
        return mailings
    mailings = Mailing.objects.all()
    cache.set(key, mailings)
    return mailings
