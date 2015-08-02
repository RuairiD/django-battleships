from django import forms
from django.contrib.auth.models import User

from players.models import Player


class UserForm(forms.ModelForm):

    class Meta:
        model = User
        fields = (
            'username',
            'password'
        )

    def __init__(self, *args, **kwargs):
        super(UserForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget = forms.TextInput(attrs={
            'class': 'form-control',
        })
        self.fields['password'].widget = forms.PasswordInput(attrs={
            'class': 'form-control',
        })


class PlayerForm(forms.ModelForm):

    class Meta:
        model = Player
        fields = ()

    def __init__(self, *args, **kwargs):
        super(PlayerForm, self).__init__(*args, **kwargs)