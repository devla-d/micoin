from django import forms
from .models import Account
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth  import login,authenticate,logout
from manager.models import VerificationCode

class RegistrationForm(UserCreationForm):
    email = forms.EmailField()
    reffered_by =forms.CharField(
                    widget=forms.TextInput(attrs={'placeholder': 'Optional- provide if any'}),required=False)
   
    class Meta:
        model = Account
        fields = ['username','email','phone','reffered_by']





class LoginForm(forms.ModelForm):
    password =  forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = Account
        fields = ['username','password']

    def clean(self):
        if self.is_valid():
            username = self.cleaned_data['username']
            password =  self.cleaned_data['password']
            if not authenticate(username=username,password=password):
                raise forms.ValidationError('Invalid Credentials')



class DepositeForm(forms.ModelForm):

    code = forms.CharField(
                    widget=forms.TextInput(attrs={'placeholder': 'Please input activation code','minlength': 5}))

    class Meta:
        model = VerificationCode
        fields = ['code']

    def clean(self):
        code = self.cleaned_data['code']
        try:
            code = VerificationCode.objects.get(code=code)
            if code.active == False:
                raise forms.ValidationError('Code in Inactive')
        except VerificationCode.DoesNotExist:
            raise forms.ValidationError('invalid code')

