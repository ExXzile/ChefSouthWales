
from django import forms
from captcha.fields import ReCaptchaField
from captcha.widgets import ReCaptchaV3
from .models import Member


class Captcha(forms.Form):
    captcha = ReCaptchaField(widget=ReCaptchaV3())


class MemberProfile(forms.Form):
    nickname = forms.CharField(max_length=24, label='nickname')
    first_name = forms.CharField(max_length=36, label='first_name')
    last_name = forms.CharField(max_length=24, label='last_name')
    email = forms.EmailField(max_length=120, label='email')
    phone = forms.CharField(max_length=120, label='phone')
    sector = forms.ChoiceField(widget=forms.Select, choices=Member.SECTORS, label='sector')
    level = forms.ChoiceField(widget=forms.Select, choices=Member.LEVELS, label='level')
    years = forms.ChoiceField(widget=forms.Select, choices=Member.YEARS, label='years')
    bio = forms.CharField(widget=forms.Textarea, label='bio')
