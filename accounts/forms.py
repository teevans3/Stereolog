from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

# Create an email field (required; add error messages)
class UserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

    # Remove autocomplete from fields
    def __init__(self, *args, **kwargs):
        super(UserCreationForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'autocomplete' : 'off'})
        self.fields['email'].widget.attrs.update({'autocomplete' : 'off'})

    def save(self, commit=True):
        user = super(UserCreationForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user

    def clean(self):
       email = self.cleaned_data.get('email')
       username = self.cleaned_data.get('username')

       if User.objects.filter(username=username).exists():
           self.add_error('username', "Username already exists.")
           raise ValidationError("Username exists.")

       if User.objects.filter(email=email).exists():
           self.add_error('email', "Email already exists.")
           raise ValidationError("Email exists.")

       return self.cleaned_data

# Remove autocomplete forms from login form
class AuthenticationForm(AuthenticationForm):

    def __init__(self, *args, **kwargs):
        super(AuthenticationForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'autocomplete' : 'off'})
