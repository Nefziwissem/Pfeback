from rest_framework import serializers
from .models import Client, File,Comment
from rest_framework import serializers
from .models import Comment
class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = '__all__'

    def validate(self, data):
        amount_given = data.get('amount_given', None)
        amount_total = data.get('amount_total', None)

        if amount_total is not None and amount_given is not None:
            if amount_given > amount_total:
                raise serializers.ValidationError("Amount given cannot be greater than the total amount.")
        return data

    def create(self, validated_data):
        client = Client(**validated_data)
        client.update_amount(validated_data['amount_given'])
        return client

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        amount_given = validated_data.get('amount_given', instance.amount_given)
        instance.amount_total = validated_data.get('amount_total', instance.amount_total)
        instance.email = validated_data.get('email', instance.email)
        instance.address = validated_data.get('address', instance.address)
        instance.phone = validated_data.get('phone', instance.phone)
        instance.is_active = validated_data.get('is_active', instance.is_active)
        instance.update_amount(amount_given)
        instance.save()
        return instance

class FileSerializer(serializers.ModelSerializer):
    class Meta:
        model = File
        fields = '__all__'
        read_only_fields = ['client']


class CommentSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(source='user.first_name', read_only=True)
    last_name = serializers.CharField(source='user.last_name', read_only=True)

    class Meta:
        model = Comment
        fields = '__all__'

