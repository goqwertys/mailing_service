from django.contrib.auth.models import AbstractUser
from django.db import models
from django_countries.fields import CountryField

from phonenumber_field.modelfields import PhoneNumberField

from users.managers import UserManager


class User(AbstractUser):
    """ Custom user model """
    username = None
    email = models.EmailField(unique=True, verbose_name='email')
    phone_number = PhoneNumberField(
        verbose_name = 'Phone Number',
        null =True,
        blank = True,
        help_text='Enter your phone number'
    )
    avatar = models.ImageField(
        upload_to='users/avatars',
        verbose_name='avatar',
        blank=True,
        null=True,
        help_text='Upload your avatar'
    )
    country = CountryField(blank=True, null=True)

    token = models.CharField(max_length=100, verbose_name='Token', blank=True, null=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'

    def __str__(self):
        return self.email
