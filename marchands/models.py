from django.db import models





class Marchand(models.Model):
    id_marchand = models.AutoField(primary_key=True)
    nom_marchand = models.CharField(max_length=100)
    type_machine = models.CharField(max_length=100)
    quantite = models.PositiveIntegerField()
    emplacement = models.CharField(max_length=255)
    date_entretien = models.DateField()
    email = models.EmailField(null=True)  # Ajouter un champ d'email

    
    def __str__(self):

        return f"{self.nom_marchand} - {self.type_machine} - {self.emplacement}"
    


class Fille(models.Model):
    fille = models.FileField(upload_to='upploads/')
    marchand = models.ForeignKey(Marchand, related_name='fichier', null=True, on_delete=models.CASCADE)
    description = models.CharField(max_length=255, blank=True, null=True)
    uploaded_at = models.DateTimeField(auto_now_add=True,null=True)

    
class Sale(models.Model):
    month = models.IntegerField()
    amount = models.FloatField()


class Vente(models.Model):
    marchand = models.ForeignKey(Marchand, related_name='ventes', on_delete=models.CASCADE)
    date_vente = models.DateField()  # Date de la vente
    montant = models.DecimalField(max_digits=10, decimal_places=2)  # Montant de la vente

    def __str__(self):
        return f"Vente de {self.marchand.nom_marchand} le {self.date_vente}"