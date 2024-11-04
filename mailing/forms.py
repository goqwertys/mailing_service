from django import forms

from mailing.models import Recipient


class StyleFormMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field, in self.fields.items():
            field.widget.attrs['class'] = 'form-control'


class RecipientForm(StyleFormMixin, forms.ModelForm):
    class Meta:
        model = Recipient
        fields = ['name', 'email', 'comment', ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].widget.attrs.update({
            'placeholder': "Enter recipient's name"
        })
        self.fields['email'].widget.attrs.update({
            'placeholder': "Enter recipient's email",
        })
        self.fields['comment'].widget.attrs.update({
            'placeholder': 'Some comment',
            'rows': 4
        })
