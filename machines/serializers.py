from rest_framework import serializers
from .models import Machine

class MachineSerializer(serializers.ModelSerializer):
    class Meta:
        model = Machine
        fields = [
            'id_machine',
            'nom_machine',
            'nom_marchand',
            'date_installation',
            'date_intervention',
            'date_mise_en_marche'
        ]