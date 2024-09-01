from django.db import models

# Create your models here.
from django.db import models

class Machine(models.Model):
    id_machine = models.AutoField(primary_key=True)
    nom_machine = models.CharField(max_length=100)
    nom_marchand = models.CharField(max_length=100)
    date_installation = models.DateField()
    date_intervention = models.DateField(null=True)



# Create your models here.

    date_mise_en_marche = models.DateField()


    def __str__(self):
        return self.nom_machine