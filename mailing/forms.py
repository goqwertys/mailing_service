from django import forms

from mailing.models import Recipient, Message, Mailing


class StyleFormMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'


class RecipientForm(StyleFormMixin, forms.ModelForm):
    class Meta:
        model = Recipient
        fields = ['name', 'email', 'comment', ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].widget.attrs.update(
            {
                'placeholder': "Enter recipient's name"
            }
        )
        self.fields['email'].widget.attrs.update(
            {
                'placeholder': "Enter recipient's email",
            }
        )
        self.fields['comment'].widget.attrs.update(
            {
                'placeholder': 'Some comment',
                'rows': 4
            }
        )


class MessageForm(StyleFormMixin, forms.ModelForm):
    class Meta:
        model = Message
        fields = ['subject', 'body']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['subject'].widget.attrs.update(
            {
                'placeholder': 'Enter subject'
            }
        )
        self.fields['body'].widget.attrs.update(
            {
                'placeholder': 'Your message here: '
            }
        )


class MailingForm(forms.ModelForm):
    class Meta:
        model = Mailing
        fields = ['message', 'recipient']

    recipient = forms.ModelMultipleChoiceField(
        queryset=Recipient.objects.all(),
        widget=forms.SelectMultiple(attrs={'class': 'form-control'})
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['message'].widget.attrs.update(
            {
                'placeholder': 'Select message',
                'class': 'form-control'
            }
        )
