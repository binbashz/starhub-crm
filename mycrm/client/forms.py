from django import forms

from .models import Client

from .models import SalesActivity

class AddClientForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = ('name', 'email', 'description',)

class SalesActivityForm(forms.ModelForm):
    class Meta:
        model = SalesActivity
        fields = ['client', 'description', 'amount', 'date']
        
        
