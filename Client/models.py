from django.db import models
from django.utils import timezone
from django.core.exceptions import ValidationError

class Client(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
    ]

    num_dossier = models.CharField(max_length=255, blank=True, null=True)
    date_signature_pv = models.DateField(blank=True, null=True)
    duree_garantie = models.IntegerField(blank=True, null=True)
    date_signature_definitif = models.DateField(blank=True, null=True)
    name = models.CharField(null=True, max_length=255)
    email = models.EmailField(null=True)
    amount_remaining = models.DecimalField(max_digits=10, decimal_places=2)
    reminder_date = models.DateTimeField(null=True, blank=True)
    email_sent = models.BooleanField(default=False)
    image = models.ImageField(upload_to='client_images/', null=True, blank=True)

    reminder_sent = models.BooleanField(default=False)
    is_paid = models.BooleanField(default=False)
    amount_total = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    amount_given = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)
    address = models.CharField(null=True, max_length=255)
    phone = models.CharField(null=True, max_length=15)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(null=True, default=timezone.now)
    purchase_date = models.DateTimeField(null=True, auto_now_add=True)

    def update_amount(self, amount_given):
        self.amount_given += amount_given
        self.amount_remaining = max(0, self.amount_total - self.amount_given)
        if self.amount_remaining == 0:
            self.status = 'completed'
        else:
            self.status = 'in_progress'
        self.save()

    def clean(self):
        if self.status == 'completed' and self.amount_given < self.amount_total:
            raise ValidationError('Amount Given must be at least equal to Amount Total to mark as completed.')

    def save(self, *args, **kwargs):
        if self.amount_given >= self.amount_total:
            self.is_paid = True
        self.amount_remaining = self.amount_total - self.amount_given
        super().save(*args, **kwargs)

class File(models.Model):
    file = models.FileField(upload_to='uploads/')
    client = models.ForeignKey(Client, related_name='files', on_delete=models.CASCADE)
    description = models.CharField(max_length=255, blank=True, null=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.file.name} - {self.client.name}"

from django.db import models
from users.models import User
from django.db import models
from django.db import models
from django.conf import settings

class Comment(models.Model):
    
    user = models.ForeignKey(User,null=True,related_name='userclient', on_delete=models.CASCADE)  # Ajout du champ user

    content = models.TextField(null=True, blank=True)
    client = models.ForeignKey('Client', null=True,on_delete=models.CASCADE)
    parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=100, null=True)
    created_at = models.DateTimeField(null=True,auto_now_add=True)
    name = models.CharField(max_length=100, null=True,blank=True)
    title = models.CharField(max_length=255, null=True, blank=True)