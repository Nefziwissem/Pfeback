from django.contrib.auth import get_user_model
from rest_framework import serializers
from .models import Rembourssement
from django.utils.translation import gettext_lazy as _



from rest_framework import serializers
from .models import Comment




from rest_framework import serializers
from django.contrib.auth import get_user_model
from users.models import Role  # Adjust this import based on your actual model location
from .models import Comment
from rest_framework import serializers
from .models import Rembourssement
from users.models import  User
from rest_framework import serializers

from rest_framework import serializers
from users.models import  User
from .models import ActionLog

User = get_user_model()
from rest_framework import serializers
from .models import Comment
from rest_framework import serializers
from .models import Comment

from rest_framework import serializers
from .models import Comment, Rembourssement

from rest_framework import serializers
from .models import Comment, Rembourssement
from rest_framework import serializers
from .models import Comment


from rest_framework import serializers
from .models import Comment

class CommentSerializer(serializers.ModelSerializer):
    created_at = serializers.DateTimeField(read_only=True)

    first_name = serializers.CharField(required=False)
    last_name = serializers.CharField(required=False)
    replies = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    class Meta:
        model = Comment
        fields = '__all__'

    def get_replies(self, obj):
        replies = obj.replies.all()
        return CommentSerializer(replies, many=True).data





User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    role_names = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = [
            'id', 'email', 'first_name', 'last_name', 'phone_number', 
            'address', 'is_staff', 'is_active', 'creation_date', 
            'expiration_date', 'status', 'roles', 'role_names'
        ]

    def get_role_names(self, obj):
        return [role.name for role in obj.roles.all()]

    def get_field_names(self, declared_fields, info):
        expanded_fields = super(UserSerializer, self).get_field_names(declared_fields, info)
        if 'roles' in expanded_fields:
            expanded_fields.remove('roles')
        return expanded_fields






from rest_framework import serializers
from .models import File
# serializers.py

from rest_framework import serializers

class RembourssementDataSerializer(serializers.Serializer):
    month = serializers.DateField()
    total_amount = serializers.DecimalField(max_digits=10, decimal_places=2)


from rest_framework import serializers
from .models import File

class FileSerializer(serializers.ModelSerializer):
    class Meta:
        model = File
        fields = ['id', 'file', 'rembourssement', 'description']
        read_only_fields = ['rembourssement']  # Ensure rembourssement is not written directly






class RembourssementSerializer(serializers.ModelSerializer):
    files = FileSerializer(many=True, read_only=True)  # Assuming you have a FileSerializer

    
    assigned_to = UserSerializer(read_only=True)

    class Meta:
        model = Rembourssement
        fields = '__all__'
        


    def save(self, **kwargs):
        # Check if request is available in context and has an authenticated user
        request = self.context.get('request')
        user = getattr(request, 'user', None)
        if user and not user.is_anonymous:
            self.validated_data['created_by'] = user
        else:
            # Handle cases where no user is authenticated or provided
            raise serializers.ValidationError("User must be authenticated to update status")
        
        return super().save(**kwargs)

    def validate_assigned_to(self, value):
        """
        Add any necessary validation for assigning users here.
        """
        return value

    def create(self, validated_data):
        # Assuming the request user is set in the view context
        user = self.context['request'].user if self.context.get('request') else None
        if 'created_by' in validated_data:
            validated_data.pop('created_by', None)
        rembourssement = Rembourssement.objects.create(**validated_data, created_by=user)
        return rembourssement



    def update(self, instance, validated_data):
        for field, value in validated_data.items():
            setattr(instance, field, value)
        instance.save()
        return instance


    def to_representation(self, instance):
        """ Modify the output format, if necessary, can be customized further """
        ret = super().to_representation(instance)
        # Add human-readable choices or any additional modifications
        status_display = dict(Rembourssement.STATUS_CHOICES).get(instance.status, instance.status)
        ret['status_display'] = _(status_display)
        return ret




class ActionLogSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()  # Ensure this displays user email or username

    class Meta:
        model = ActionLog
        fields = ['created_at', 'action', 'description', 'user']
