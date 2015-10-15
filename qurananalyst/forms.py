from registration.forms import RegistrationForm
from captcha.fields import ReCaptchaField
from django.forms.forms import Form
from django.forms.models import ModelForm
from models import Comment
from django import forms

class RegistrationFormCaptcha(RegistrationForm):
    captcha = ReCaptchaField(attrs={'theme' : 'clean'})


class VerseCommentForm(ModelForm):
    class Meta:
        model = Comment
        widgets = {
            'ctext': forms.Textarea(attrs=dict(rows=2, cols=71)),
            'vnum': forms.HiddenInput(),
            'cnum': forms.HiddenInput(),
            'user': forms.HiddenInput()
        }
    captcha = ReCaptchaField(attrs={'theme' : 'clean'})