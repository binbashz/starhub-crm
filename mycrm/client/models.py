from django.contrib.auth.models import User
from django.db import models
from team.models import Team


class Client(models.Model):
    team = models.ForeignKey(Team, related_name='clients', on_delete=models.CASCADE)
    name = models.CharField(max_length=225)
    email = models.EmailField()
    description = models.TextField(blank=True, null=True)
    created_by = models.ForeignKey(User, related_name='clients', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ('name',)

    def __str__(self):
        return self.name 
    

class SalesActivity(models.Model):
    client = models.ForeignKey(Client, related_name='sales_activities', on_delete=models.CASCADE)
    description = models.TextField()
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField()
    created_by = models.ForeignKey(User, related_name='sales_activities', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('-date',)

    def __str__(self):
        return f"Sales activity for {self.client.name} - {self.date}"
