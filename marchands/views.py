from django.shortcuts import render
from django.views import View
from rest_framework import generics
from .models import Marchand
from .serializers import MarchandSerializer
from rest_framework.parsers import MultiPartParser, FormParser
from django.http import FileResponse, JsonResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .tasks import send_reminder_ematil  # Tâche Celery pour envoyer l'email

# Vue pour lister et créer des Marchands
class MarchandListCreate(generics.ListCreateAPIView):
    queryset = Marchand.objects.all()
    serializer_class = MarchandSerializer
    parser_classes = (MultiPartParser, FormParser)

# Vue pour récupérer, mettre à jour ou supprimer un Marchand
class MarchandDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Marchand.objects.all()
    serializer_class = MarchandSerializer

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Marchand
from .serializers import MarchandSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Marchand
from .serializers import MarchandSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Marchand
from .serializers import MarchandSerializer
from .tasks import send_reminder_ematil

@api_view(['POST'])
def create_marchand(request):
    if request.method == 'POST':
        serializer = MarchandSerializer(data=request.data)
        if serializer.is_valid():
            marchand = serializer.save()
            if marchand.date_entretien:
                send_reminder_ematil.apply_async((marchand.id_marchand,), eta=marchand.date_entretien)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class SendReminderView(View):
    def get(self, request, *args, **kwargs):
        send_reminder_ematil()
        return JsonResponse({"status": "Reminders sent"})
    


from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from .models import Marchand, Fille
from .serializers import FilleSerializer

from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from .models import  Fille
from .serializers import FilleSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.views import APIView
from .models import Fille
from .serializers import FilleSerializer
from django.shortcuts import get_object_or_404

from .models import Marchand

from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from .models import Marchand, Fille
from .serializers import FilleSerializer

class FilleUploadView(APIView):
    parser_classes = [MultiPartParser, FormParser]

    def post(self, request, *args, **kwargs):
        marchand_id = kwargs.get('marchand_id')
        marchand = get_object_or_404(Marchand, pk=marchand_id)
        serializer = FilleSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(marchand=marchand)
            return Response({
                'message': 'File uploaded successfully',
                'file': serializer.data
            }, status=status.HTTP_201_CREATED)
        return Response({
            'message': 'File upload failed',
            'errors': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)

class FilleDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Fille.objects.all()
    serializer_class = FilleSerializer
    lookup_field = 'pk'

class FilleDownloadView(APIView):
    def get(self, request, fille_id):
        fille = get_object_or_404(Fille, id=fille_id)
        response = FileResponse(fille.fille, as_attachment=True)
        return response

class FilleDeleteView(APIView):
    def delete(self, request, marchand_id, fille_id):
        fille = get_object_or_404(Fille, marchand_id=marchand_id, id=fille_id)
        fille.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    
class DocumentAssignmentView(APIView):
    def post(self, request, *args, **kwargs):
        marchand_id = request.data.get('marchandId')
        if marchand_id:
            return Response({'message': 'Document assigned successfully!'}, status=status.HTTP_200_OK)
        return Response({'error': 'marchand ID is required'}, status=status.HTTP_400_BAD_REQUEST)
    



    
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from .models import Fille

class FilleDeleteView(APIView):
    def delete(self, request, marchand_id, Fille_id):
        Fille = get_object_or_404(Fille, marchand_id=marchand_id, id=Fille_id)
        Fille.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

# Vue pour lister et créer des Marchands
from django.http import JsonResponse
from .models import Sale
import numpy as np
from sklearn.linear_model import LinearRegression

import logging
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from sklearn.linear_model import LinearRegression
import numpy as np
from .models import Sale

import logging
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from sklearn.linear_model import LinearRegression
import numpy as np
from .models import Sale
import logging
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from sklearn.linear_model import LinearRegression
import numpy as np
from .models import Sale

logger = logging.getLogger(__name__)

def train_model():
    try:
        sales = Sale.objects.all().values('month', 'amount')
        if not sales:
            logger.error("No sales data found.")
            raise ValueError("No sales data found.")
        X = np.array([sale['month'] for sale in sales]).reshape(-1, 1)
        y = np.array([sale['amount'] for sale in sales])
        
        model = LinearRegression().fit(X, y)
        return model
    except Exception as e:
        logger.error(f"Error training model: {str(e)}")
        raise

@require_http_methods(["GET"])
def sales_data(request):
    try:
        model = train_model()
        sales = Sale.objects.all().values('month', 'amount')
        if not sales:
            logger.error("No sales data found.")
            return JsonResponse({'error': 'No sales data found.'}, status=404)
        
        X = np.array([sale['month'] for sale in sales]).reshape(-1, 1)
        predictions = model.predict(X)
        
        data = {
            'labels': [sale['month'] for sale in sales],
            'datasets': [
                {
                    'label': 'Actual Sales',
                    'data': [sale['amount'] for sale in sales],
                },
                {
                    'label': 'Predicted Sales',
                    'data': predictions.tolist(),
                }
            ]
        }
        return JsonResponse(data)
    except Exception as e:
        logger.error(f"Error in sales_data view: {str(e)}")
        return JsonResponse({'error': 'Internal Server Error'}, status=500)
    




    from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Marchand, Vente
from django.shortcuts import get_object_or_404

class MarchandSalesView(APIView):
    def get(self, request, marchand_id):
        marchand = get_object_or_404(Marchand, id=marchand_id)
        ventes = Vente.objects.filter(marchand=marchand).order_by('date_vente')
        data = [{'date': vente.date_vente, 'amount': vente.montant} for vente in ventes]
        return Response(data, status=status.HTTP_200_OK)