from django.contrib import admin

from mailing.models import Recipient, Message, Mailing


@admin.register(Recipient)
class RecipientAdmin(admin.ModelAdmin):
    list_display = ('id','email', 'name', 'comment')
    search_fields = ('name', 'comment')
    list_filter = ('name', 'comment')
    ordering = ('id', )

@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('id','subject', 'body', )
    search_fields = ('subject', 'body')
    list_filter = ('subject',)
    ordering = ('id', )

@admin.register(Mailing)
class MailingAdmin(admin.ModelAdmin):
    list_display = ('id', 'first_send', 'end_send', 'status')
    search_fields = ('status', )
    list_filter = ('status', )
    ordering = ('id', )
