from django import forms
from .models import VerificationCode




class CodeForm(forms.ModelForm):
    class Meta:
        model = VerificationCode
        fields = ['name','package']