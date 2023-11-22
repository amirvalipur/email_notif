from django import forms
from .models import CustomUser
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import ReadOnlyPasswordHashField


class UserCreationForm(forms.ModelForm):
    password1 = forms.CharField(max_length=50, label='رمز عبور', widget=forms.PasswordInput)
    password2 = forms.CharField(max_length=50, label='تکرار رمز عبور', widget=forms.PasswordInput)

    class Meta:
        model = CustomUser
        fields = ['email_address', 'name', 'family']

    def clean_password2(self):
        pass1 = self.cleaned_data.get('password1')
        pass2 = self.cleaned_data.get('password2')
        if pass1 and pass2 and pass1 != pass2:
            raise ValidationError('رمز عبور و تکرار آن با هم مغایرت دارند')
        return pass2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        if commit:
            user.save()
        return user


# _______________________________________________________________________
class UserChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField(help_text="<a href=../password > فراموشی رمز عبور <a/>")

    class Meta:
        model = CustomUser
        fields = ['email_address', 'password', 'name', 'family', 'is_active', 'is_admin',
                  'is_superuser']
