from django.shortcuts import render


from datetime import timezone
from django.views import View
from rest_framework import generics
from .models import Machine
from .serializers import MachineSerializer

from django.http import JsonResponse
from rest_framework.views import APIView
from django.utils import timezone
# ListCreateAPIView permet de lister toutes les machines et d'en créer de nouvelles
class MachineListCreate(generics.ListCreateAPIView):
    queryset = Machine.objects.all()
    serializer_class = MachineSerializer

# RetrieveUpdateDestroyAPIView permet de récupérer, mettre à jour et supprimer une machine spécifique
class MachineDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Machine.objects.all()
    serializer_class = MachineSerializer




import pytz
from django.utils import timezone
from django.http import JsonResponse
from django.views import View
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

from datetime import timedelta

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from django.utils import timezone
from .models import Machine
from .serializers import MachineSerializer
from .tasks import send_machine_reminder_email  # Assurez-vous que cette tâche est définie

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Machine
from .serializers import MachineSerializer
from .tasks import send_machine_reminder_email
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Machine

@api_view(['DELETE'])
def delete_machine(request, id_machine):
    try:
        machine = Machine.objects.get(id_machine=id_machine)
        machine.delete()
        return Response({'message': 'Machine supprimée avec succès.'}, status=status.HTTP_204_NO_CONTENT)
    except Machine.DoesNotExist:
        return Response({'error': 'Machine non trouvée.'}, status=status.HTTP_404_NOT_FOUND)

@api_view(['POST'])
def create_machine(request):
    if request.method == 'POST':
        serializer = MachineSerializer(data=request.data)
        if serializer.is_valid():
            machine = serializer.save()
            # Planifiez la tâche d'envoi de l'email de rappel deux minutes après la création
            send_machine_reminder_email.apply_async((machine.id_machine,), countdown=120)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class SendMachineRemindersView(APIView):
    def get(self, request, *args, **kwargs):
        now = timezone.now().date()  # On travaille avec des dates ici
        machines = Machine.objects.filter(
            date_intervention__lte=now
        )

        if not machines.exists():
            return Response({'message': 'No machines found for intervention reminders.'}, status=status.HTTP_404_NOT_FOUND)

        for machine in machines:
            send_machine_reminder_email.delay(machine.id_machine)

        serializer = MachineSerializer(machines, many=True)
        return Response({'message': 'Reminder emails sent successfully.', 'machines': serializer.data}, status=status.HTTP_200_OK)