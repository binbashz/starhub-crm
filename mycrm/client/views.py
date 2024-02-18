from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect

from .forms import AddClientForm
from .models import Client
from team.models import Team

from .models import SalesActivity
from .forms import SalesActivityForm

@login_required
def clients_list(request):
    clients = Client.objects.filter(created_by=request.user)
    
    return render(request, 'client/clients_list.html', {
        'clients': clients
        })

@login_required
def clients_detail(request, pk):
    client = get_object_or_404(Client, created_by=request.user, pk=pk)
    
    return render(request, 'client/clients_detail.html', {
        'client': client
        })
    
@login_required
def client_add(request):
    team = Team.objects.filter(created_by=request.user)[0]
    if request.method == 'POST':
        form = AddClientForm(request.POST)
        
        if form.is_valid():
            team = Team.objects.filter(created_by=request.user)[0]
            client = form.save(commit=False)
            client.created_by = request.user
            client.team = team
            client.save()
            
            messages.success(request, "The client was created.")
            
            return redirect('clients:list')
    else:
        
        form = AddClientForm()

    return render(request, 'client/clients_add.html', {
        'form': form,
        'team': team
        
    })
    
@login_required
def clients_edit(request, pk):
    client = get_object_or_404(Client, created_by=request.user, pk=pk)
    
    if request.method == 'POST':
        form = AddClientForm(request.POST, instance=client)
        if form.is_valid():
            form.save()
        
        messages.success(request, "The changes was saved.")
        return redirect('clients:list')
    else:
        form = AddClientForm(instance=client)
        
        return render(request, 'client/clients_edit.html', {
        'form': form
    })
    
@login_required
def client_delete(request, pk):
    client = get_object_or_404(Client, created_by=request.user, pk=pk)
    client.delete()
    
    messages.success(request, "The client was deleted.")
    
    return redirect('clients:list')

@login_required
def list_sales_activities(request):
    sales_activities = SalesActivity.objects.all()
    return render(request, 'list_sales_activities.html', {'sales_activities': sales_activities})

@login_required
def create_sales_activity(request):
    if request.method == 'POST':
        form = SalesActivityForm(request.POST)
        if form.is_valid():
            sales_activity = form.save(commit=False) 
            sales_activity.created_by = request.user
            sales_activity.save() 
            return redirect('clients:list_sales_activities')
    else:
        form = SalesActivityForm()
    return render(request, 'create_sales_activity.html', {'form': form})
