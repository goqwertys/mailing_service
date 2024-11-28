from django.core.mail import send_mail
from django.utils import timezone

from .models import Mailing, Attempt

def send_mailing(mailing_id, user):
    mailing = Mailing.objects.get(id=mailing_id)

    if mailing.status in ('CPL', 'DSBL'):
        raise ValueError('This mailing cannot be sent.')

    recipients = mailing.recipient.all()
    message = mailing.message

    mailing.status = 'LCH'
    mailing.start_of_sending = timezone.now()
    mailing.save()

    for recipient in recipients:
        try:
            send_mail(
                subject=message.subject,
                message=message.body,
                from_email=None,
                recipient_list=[recipient.email]
            )
            status = 'CM'
            response = 'Email send successfully'
        except Exception as e:
            status = 'FL'
            response = str(e)

        attempt = Attempt(
            dt=timezone.now(),
            status=status,
            response=response,
            mailing=mailing,
            user=user
        )
        attempt.save()

    mailing.status = 'CPL'
    mailing.end_of_sending = timezone.now()
    mailing.save()
