from django import forms
from django.contrib.auth.models import User

from members.models import Member


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('username', 'email', 'password')


class MemberForm(forms.ModelForm):

    class Meta:
        model = Member
        fields = (
            'twitter_username',
            'instagram_username',
            'profile_visible'
        )