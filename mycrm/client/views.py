from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect

from .forms import AddClientForm
from .models import Client
from team.models import Team

from .models import SalesActivity
from .forms import SalesActivityForm
from .models import SalesActivity

from django.http import HttpResponse
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import Paragraph

from django.conf import settings
from django.http import JsonResponse
from client.models import Client
import os
from .models import SalesActivity


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


def delete_sales_activity(request, pk):
    activity = get_object_or_404(SalesActivity, pk=pk)
    if request.method == 'POST':
        activity.delete()
        
        messages.success(request, 'The sales activity has been successfully deleted.')
        
        sales_activities = SalesActivity.objects.all()
        return render(request, 'list_sales_activities.html', {'sales_activities': sales_activities})
    
    return redirect('clients:list_sales_activities')



def generate_invoice(request):
    if request.method == 'POST':
        # Retrieve form data
        client_name = request.POST.get('client_name')
        client_address = request.POST.get('client_address')
        client_contact = request.POST.get('client_contact')
        client_tax_id = request.POST.get('client_tax_id')

        company_name = request.POST.get('company_name')
        company_address = request.POST.get('company_address')
        company_phone = request.POST.get('company_phone')
        company_email = request.POST.get('company_email')
        company_tax_id = request.POST.get('company_tax_id')

        invoice_number = request.POST.get('invoice_number')
        invoice_date = request.POST.get('invoice_date')

        items = request.POST.getlist('item')
        quantities = request.POST.getlist('quantity')
        unit_prices = request.POST.getlist('unit_price')
        totals = request.POST.getlist('total')

        total_amount = request.POST.get('total_amount')
        payment_method = request.POST.get('payment_method')
        due_date = request.POST.get('due_date')

        # Generate PDF
        pdf_filename = "invoice.pdf"
        generate_pdf(client_name, client_address, client_contact, client_tax_id,
                     company_name, company_address, company_phone, company_email, company_tax_id,
                     invoice_number, invoice_date,
                     items, quantities, unit_prices, totals,
                     total_amount, payment_method, due_date, pdf_filename)

        # Redirect to index
        return redirect('index')

    return render(request, 'generate_invoice.html')




def generate_pdf(client_name, client_address, client_contact, client_tax_id,
                 company_name, company_address, company_phone, company_email, company_tax_id,
                 invoice_number, invoice_date,
                 items, quantities, unit_prices, totals,
                 total_amount, payment_method, due_date, pdf_filename):
    # Create PDF document
    doc = SimpleDocTemplate(pdf_filename, pagesize=letter)

    # Content of the invoice
    content = [
        ["Invoice Number:", invoice_number],
        ["Invoice Date:", invoice_date],
        ["", ""],  
        ["Client:", ""],
        ["Name:", client_name],
        ["Address:", client_address],
        ["Contact:", client_contact],
        ["Tax ID:", client_tax_id],
        ["", ""],  
        ["Company:", ""],
        ["Name:", company_name],
        ["Address:", company_address],
        ["Phone:", company_phone],
        ["Email:", company_email],
        ["Tax ID:", company_tax_id],
        ["", ""],  # Empty row for spacing
        ["Description", "Quantity", "Unit Price", "Total"]
    ]

    # Add items to the table
    for item, quantity, unit_price, total in zip(items, quantities, unit_prices, totals):
        content.append([item, quantity, unit_price, total])

    # Add total and payment details
    content.extend([
        ["", "", "", ""],  # Empty row for spacing
        ["Total Amount:", "", "", total_amount],
        ["Payment Method:", "", "", payment_method],
        ["Due Date:", "", "", due_date]
    ])

    # Define styles
    styles = getSampleStyleSheet()
    heading_style = styles["Heading1"]
    paragraph_style = styles["BodyText"]

    # Create Paragraphs for heading and content
    heading = Paragraph("Invoice", heading_style)
    content_paragraphs = [Paragraph(f"{row[0]} {row[1]}", paragraph_style) for row in content]

    # Define table style
    table_style = TableStyle([('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                              ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                              ('GRID', (0, 0), (-1, -1), 1, colors.black)])

    # Create table for the invoice
    table = Table(content, colWidths=[250, 70, 70, 90], hAlign='LEFT')
    table.setStyle(table_style)

    # Build PDF document
    doc.build([heading] + [Spacer(1, 20)] + content_paragraphs + [Spacer(1, 20), table])
    


def download_invoice(request):
    
    pdf_filename = "invoice.pdf"
    pdf_path = os.path.join(settings.BASE_DIR, pdf_filename)

    
    if os.path.exists(pdf_path):
       
        with open(pdf_path, 'rb') as pdf_file:
            response = HttpResponse(pdf_file.read(), content_type='application/pdf')
            response['Content-Disposition'] = 'attachment; filename="invoice.pdf"'
            return response
    else:
        return HttpResponse("File not found, no recent files generated for download", status=404)


def sales_activities_per_client(request):
    clients = Client.objects.all()
    data = []
    for client in clients:
        activities_count = client.sales_activities.count()
        data.append({'client': client.name, 'activities_count': activities_count})

    
    return render(request, 'sales-activities-per-client.html', {'data': data})



def delete_sales_activity(request, pk):
    activity = get_object_or_404(SalesActivity, pk=pk)
    if request.method == 'POST':
        activity.delete()
        
        clients = Client.objects.all()
        data = [{'client': client.name, 'activities_count': client.sales_activities.count()} for client in clients]
        return render(request, 'sales-activities-per-client.html', {'data': data})
    return render(request, 'sales-activities-per-client.html')  