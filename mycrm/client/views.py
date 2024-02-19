from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect

from .forms import AddClientForm
from .models import Client
from team.models import Team

from .models import SalesActivity
from .forms import SalesActivityForm

from django.http import HttpResponse
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle


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




def generate_invoice(request):
    if request.method == 'POST':
        # Retrieve form data
        client = request.POST.get('client')
        quantity = request.POST.get('quantity')
        unit_price = request.POST.get('unit_price')

        # Generate PDF
        pdf_filename = "invoice.pdf"
        generate_pdf(client, quantity, unit_price, pdf_filename)

        # Redirect to index
        return redirect('index')

    return render(request, 'generate_invoice.html')

def generate_pdf(client, quantity, unit_price, pdf_filename):
    # Create PDF document
    doc = SimpleDocTemplate(pdf_filename, pagesize=letter)
    
    # Content of the invoice
    content = [
        ["Client", "Quantity", "Unit Price"],
        [client, quantity, unit_price]
    ]
    
    # Create table for the invoice
    table = Table(content, colWidths=[200, 100, 100])
    table.setStyle(TableStyle([('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                               ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                               ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                               ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                               ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                               ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                               ('GRID', (0, 0), (-1, -1), 1, colors.black)]))
    
    # Add table to the document
    doc.build([table])
    
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.conf import settings
import os

def download_invoice(request):
    # Ruta al archivo PDF generado
    pdf_filename = "invoice.pdf"
    pdf_path = os.path.join(settings.BASE_DIR, pdf_filename)

    # Verifica si el archivo existe
    if os.path.exists(pdf_path):
        # Abre el archivo PDF y devuelve como respuesta
        with open(pdf_path, 'rb') as pdf_file:
            response = HttpResponse(pdf_file.read(), content_type='application/pdf')
            response['Content-Disposition'] = 'attachment; filename="invoice.pdf"'
            return response
    else:
        return HttpResponse("File not found", status=404)
