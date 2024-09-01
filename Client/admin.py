from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Client

class ClientAdmin(admin.ModelAdmin):
    list_display = ['num_dossier', 'date_signature_pv', 'duree_garantie', 'date_signature_definitif']  # Add other fields as needed

admin.site.register(Client, ClientAdmin)
