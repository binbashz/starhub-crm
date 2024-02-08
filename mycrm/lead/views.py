from typing import Any
from django.contrib.auth.decorators import login_required
from django.db.models.base import Model as Model
from django.db.models.query import QuerySet
from django.forms.models import BaseModelForm
from django.http import HttpResponse
from django.utils.decorators import method_decorator
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, DeleteView, UpdateView, CreateView

from .forms import AddLeadForm
from .models import Lead

from client.models import Client
from team.models import Team

class LeadListView(ListView):
    model = Lead
    
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_queryset(self):
        queryset = super(LeadListView,self).get_queryset()
        
        return queryset.filter(created_by=self.request.user, converted_to_client=False)
    
    
class LeadDetailView(DetailView):
    model = Lead
    
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)
    
    def get_queryset(self):
        queryset = super(LeadDetailView,self).get_queryset()
        
        return queryset.filter(created_by=self.request.user, pk=self.kwargs.get('pk'))
        
class LeadDeleteView(DeleteView):
    model = Lead
    success_url = reverse_lazy('leads:list')

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_queryset(self):
        queryset = super(LeadDeleteView, self).get_queryset()

        return queryset.filter(created_by=self.request.user, pk=self.kwargs.get('pk'))
    
    def get(self, request, *args, **kwargs):
            return self.post(request, *args, **kwargs)


class LeadUpdateView(UpdateView):
    model = Lead
    fields = ('name', 'email', 'description', 'priority', 'status',)
    
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)
    
    def get_queryset(self):
        queryset = super(LeadUpdateView, self).get_queryset()

        return queryset.filter(created_by=self.request.user, pk=self.kwargs.get('pk'))
    
    def get_success_url(self):
        return reverse_lazy('leads:list')
     

class LeadCreatedView(CreateView):
    model = Lead
    fields = ('name', 'email', 'description', 'priority', 'status',)
    
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)
    
    def get_success_url(self):
        return reverse_lazy('leads:list')
    
    def form_valid(self, form):
        team = Team.objects.filter(created_by=self.request.user)[0]
        
        self.object = form.save(commit=False)
        self.object.created_by = self.request.user 
        self.object.team = team
        self.object.save()
        return redirect(self.get_success_url())



@login_required
def converted_to_client(request, pk):
     lead = get_object_or_404(Lead, created_by=request.user, pk=pk)
     team = Team.objects.filter(created_by=request.user)[0]
     
     client = Client.objects.create(
         name=lead.name,
         email=lead.email,
         description=lead.description,
         created_by=request.user,
         team = team,
         )
     
     lead.converted_to_client = True
     lead.save()
     
     messages.success(request, "The lead was converted to a client.")
     
     return redirect('leads:list')