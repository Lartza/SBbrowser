from django import forms


class VideoIDForm(forms.Form):
    videoid = forms.CharField(label='VideoID', max_length=64)


class UsernameForm(forms.Form):
    username = forms.CharField(label='Username', max_length=128)


class UserIDForm(forms.Form):
    userid = forms.CharField(label='UserID', max_length=128)


class UUIDForm(forms.Form):
    uuid = forms.CharField(label='UUID', max_length=128)
