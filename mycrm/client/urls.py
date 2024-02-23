from django.urls import path
from . import views
from client.views import sales_activities_per_client


app_name = 'clients'

urlpatterns = [
    path('', views.clients_list, name='list'),
    path('<int:pk>/', views.clients_detail, name='detail'),
    path('<int:pk>/delete/', views.client_delete, name='delete'),
    path('<int:pk>/edit/', views.clients_edit, name='edit'),
    path('add/', views.client_add, name='add'),
    path('sales-activities/', views.list_sales_activities, name='list_sales_activities'),
    path('create-sales-activity/', views.create_sales_activity, name='create_sales_activity'),
    path('sales_activities/<int:pk>/delete/', views.delete_sales_activity, name='delete_sales_activity'),
    path('generate-invoice/', views.generate_invoice, name='generate_invoice'),
    path('download-invoice/', views.download_invoice, name='download_invoice'),
    path('sales-activities-per-client/', views.sales_activities_per_client, name='sales_activities_per_client'),
    path('sales-activities/<int:pk>/delete/', views.delete_sales_activity, name='delete_sales_activity'),

   ]
