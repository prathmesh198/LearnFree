from django import forms
from django.contrib.auth.models import User
from .models import course


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput) 

    class Meta:
        model = User  
        fields = ['username', 'email', 'password']



class LoginForm(forms.Form):
    username = forms.CharField(max_length=100)
    password = forms.CharField(widget=forms.PasswordInput)


class CourseForm(forms.ModelForm):
    class Meta:
        model = course
        fields = '__all__'