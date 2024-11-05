from django.core.validators import EmailValidator
from django.db import models


class Recipient(models.Model):
    """ Mailing model"""
    email = models.EmailField(
        unique=True,
        max_length=254,
        validators=[EmailValidator(message='Enter a valid email address')],
        verbose_name='Email Address'
    )
    name = models.CharField(max_length=255)
    comment = models.TextField()

    def __str__(self):
        return f'{self.email} {self.name}'

    class Meta:
        verbose_name = 'recipient'
        verbose_name_plural = 'recipients'


class Message(models.Model):
    """ Message model """
    subject = models.CharField(max_length=255)
    body = models.TextField()

    def __str__(self):
        return f'{self.subject} {self.body[:20]}'

    class Meta:
        verbose_name = 'message'
        verbose_name_plural = 'messages'


class Mailing(models.Model):
    start_of_sending = models.DateTimeField(blank=True, null=True)
    end_of_sending = models.DateTimeField(blank=True, null=True)

    STATUS_CHOICES = [
        ('CPL', 'Completed'),
        ('CRT', 'Created'),
        ('LCH', 'Launched'),
    ]
    status = models.CharField(
        max_length=3,
        choices=STATUS_CHOICES,
        default='CRT',
        verbose_name='Mailing status'
    )
    message = models.ForeignKey(Message, on_delete=models.CASCADE, related_name='mailings')
    recipient = models.ManyToManyField(Recipient)

    def __str__(self):
        return f'Mailing {self.id} - {self.status}'

    class Meta:
        verbose_name = 'mailing'
        verbose_name_plural = 'mailings'


class Attempt(models.Model):
    dt = models.DateTimeField()
    STATUS_CHOICES = [
        ('CM', 'Completed'),
        ('CR', 'Created'),
        ('LN', 'Launched'),
    ]

    status = models.CharField(
        max_length=3,
        choices=STATUS_CHOICES,
        default='CRT',
        verbose_name='Mailing attempt'
    )

    response = models.TextField()
    mailing = models.ForeignKey(Mailing, on_delete=models.CASCADE, related_name='attempts')
