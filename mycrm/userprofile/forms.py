from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from team.models import Plan
from .models import Userprofile

INPUT_CLASS = 'w-full my-4 py-4 px-6 rounded-xl bg-gray-100'


class SignupForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

    username = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': 'Your username',
        'class': INPUT_CLASS
    }))
    email = forms.CharField(widget=forms.EmailInput(attrs={
        'placeholder': 'Your email address',
        'class': INPUT_CLASS
    }))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': 'Your password',
        'class': INPUT_CLASS
    }))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': 'Repeat password',
        'class': INPUT_CLASS
    }))

    # Crear un campo de elección con los planes disponibles
    plan = forms.ChoiceField(choices=[], widget=forms.RadioSelect(attrs={
        'class': INPUT_CLASS
    }))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['plan'].choices = [(plan.id, plan.name) for plan in Plan.objects.all()]

    def label_suffix(self):
        return ''  
    
    
    

class ProfileForm(forms.ModelForm):
    # Este formulario permite al usuario cambiar su email y su imagen de perfil
    email = forms.EmailField(required=True)

    class Meta:
        model = Userprofile
        fields = ['email', 'avatar']

    def clean_email(self):
        
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exclude(username=self.instance.user.username).exists():
            raise forms.ValidationError('This email address is already in use.')
        return email

    def save(self, commit=True):
        
        user = self.instance.user
        user.email = self.cleaned_data['email']
        user.save()
        profile = super(ProfileForm, self).save(commit=False)
        profile.user = user
        if commit:
            profile.save()
        return profile