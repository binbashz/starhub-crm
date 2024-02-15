from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from team.models import Plan

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
        return ''  # Eliminar los dos puntos después de la etiqueta del campo
