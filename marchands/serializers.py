from rest_framework import serializers
from .models import Fille, Marchand, Sale

class MarchandSerializer(serializers.ModelSerializer):

    class Meta:
        model = Marchand
        fields = '__all__'  # Ou spécifiez les champs explicitement
class FilleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Fille
        fields = '__all__'


class SaleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sale
        fields = '_all_'        