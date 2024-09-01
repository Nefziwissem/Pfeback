from django.shortcuts import get_object_or_404
from django.utils import timezone
from rest_framework import status, generics, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from django.http import JsonResponse, FileResponse
from rest_framework.views import APIView

from django.views.decorators.csrf import csrf_exempt

from django.core.mail import send_mail
from datetime import timedelta
from django.utils import timezone

from django.core.management import call_command
from .models import Client, File
from .serializers import ClientSerializer, FileSerializer
from rest_framework import generics
from .models import File
from .serializers import FileSerializer

class ClientDocumentsView(generics.ListAPIView):
    serializer_class = FileSerializer

    def get_queryset(self):
        client_id = self.kwargs.get('client_id')
        return File.objects.filter(client_id=client_id)

class ClientListView(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    queryset = Client.objects.all()
    serializer_class = ClientSerializer

class ClientDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer
    lookup_field = 'pk'

    def get(self, request, *args, **kwargs):
        client = self.get_object()
        serializer = self.get_serializer(client)
        client_data = serializer.data

        if client.reminder_date:
            now = timezone.localtime()
            reminder_date_local = timezone.localtime(client.reminder_date)
            time_diff = reminder_date_local - now

            days, seconds = divmod(time_diff.total_seconds(), 86400)
            hours, seconds = divmod(seconds, 3600)
            minutes = seconds // 60

            client_data['reminder_date'] = reminder_date_local.strftime('%d/%m/%Y %H:%M:%S')
            client_data['time_until_reminder'] = f"{int(days)} days, {int(hours)} hours, {int(minutes)} minutes"

            if time_diff <= timedelta(0) and not client.email_sent:
                try:
                    send_mail(
                        'Reminder: Payment Due',
                        'This is a reminder that your payment is due.',
                        'samaraouadi7@gmail.com',
                        [client.email],
                        fail_silently=False,
                    )
                    client.email_sent = True
                    client.save(update_fields=['email_sent'])
                except Exception as e:
                    return Response({'error': f'Failed to send email: {str(e)}'}, status=500)

        files = File.objects.filter(client=client)
        file_serializer = FileSerializer(files, many=True)
        client_data['files'] = file_serializer.data
        return Response(client_data)
from rest_framework.parsers import MultiPartParser, FormParser  # Import the parsers here
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Client

@api_view(['PATCH'])
def toggle_active(request, pk):
    try:
        client = Client.objects.get(pk=pk)
        client.is_active = not client.is_active
        client.save()
        return Response({'is_active': client.is_active}, status=status.HTTP_200_OK)
    except Client.DoesNotExist:
        return Response({'error': 'Client not found'}, status=status.HTTP_404_NOT_FOUND)

from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Client
from .serializers import ClientSerializer
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Client
from .serializers import ClientSerializer

@api_view(['PUT', 'PATCH'])
def update_client(request, pk):
    try:
        client = Client.objects.get(pk=pk)
    except Client.DoesNotExist:
        return Response({'error': 'Client not found'}, status=status.HTTP_404_NOT_FOUND)

    serializer = ClientSerializer(client, data=request.data, partial=True)  # Use partial=True for PATCH
    if serializer.is_valid():
        updated_client = serializer.save()
        return Response(ClientSerializer(updated_client).data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
from .tasks import send_reminder_email

@api_view(['POST'])
def create_client(request):
    if request.method == 'POST':
        serializer = ClientSerializer(data=request.data)
        if serializer.is_valid():
            client = serializer.save()
            # Trigger a task to send a reminder email if amount remaining is greater than zero
            if client.amount_remaining > 0 and client.reminder_date:
                send_reminder_email.apply_async((client.id,), eta=client.reminder_date)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class SendPaymentRemindersView(APIView):
    def get(self, request, *args, **kwargs):
        now = timezone.now()
        clients = Client.objects.filter(
            amount_remaining__gt=0,
            reminder_date__lte=now
        )

        if not clients.exists():
            return Response({'message': 'No clients found with unpaid amounts or reminders already sent.'}, status=status.HTTP_404_NOT_FOUND)

        for client in clients:
            send_reminder_email.delay(client.id)

        serializer = ClientSerializer(clients, many=True)
        return Response({'message': 'Reminder emails sent successfully.', 'clients': serializer.data}, status=status.HTTP_200_OK)

@csrf_exempt
@api_view(['POST'])
def trigger_send_reminders_view(request):
    call_command('send_reminders')
    return JsonResponse({'status': 'success', 'message': 'Reminder emails triggered'})

class ClientCheckUnpaidView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        period = timedelta(minutes=10)
        threshold_date = timezone.now() - period

        clients = Client.objects.filter(
            amount_remaining__gt=0,
            created_at__lte=threshold_date
        )

        if not clients.exists():
            return Response({'message': 'No clients found with unpaid amounts.'})

        for client in clients:
            try:
                send_mail(
                    'Reminder: Payment Due',
                    f'Dear {client.name},\n\nYou have an outstanding amount of {client.amount_remaining}. Please make the payment at your earliest convenience.',
                    'samaraouadi7@gmail.com',
                    [client.email],
                    fail_silently=False,
                )
            except Exception as e:
                return Response({'error': f'Failed to send email to {client.email}: {e}'}, status=500)

        return Response({'message': 'Reminder emails sent.'})
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from .models import Client, File
from .serializers import FileSerializer

from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from .models import Client, File
from .serializers import FileSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.views import APIView
from .models import Client, File
from .serializers import FileSerializer
from django.shortcuts import get_object_or_404

class FileUploadView(APIView):
    parser_classes = [MultiPartParser, FormParser]

    def post(self, request, *args, **kwargs):
        client_id = kwargs.get('client_id')
        client = get_object_or_404(Client, pk=client_id)
        serializer = FileSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(client=client)
            return Response({
                'message': 'File uploaded successfully',
                'file': serializer.data
            }, status=status.HTTP_201_CREATED)
        return Response({
            'message': 'File upload failed',
            'errors': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)


from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from .models import File

def delete_file(request, file_id):
    file = get_object_or_404(File, id=file_id)
    file.delete()
    return JsonResponse({'status': 'success'})
from rest_framework.permissions import IsAuthenticated

from django.http import FileResponse
from django.shortcuts import get_object_or_404
from .models import File
from django.shortcuts import get_object_or_404
from django.http import FileResponse
from .models import File
from django.http import FileResponse, Http404
from .models import File
# views.py
from rest_framework.permissions import IsAuthenticated

class FileDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = File.objects.all()
    serializer_class = FileSerializer
    lookup_field = 'pk'



class FileDownloadView(APIView):
    def get(self, request, file_id):
        file = get_object_or_404(File, id=file_id)
        response = FileResponse(file.file, as_attachment=True)
        return response
    
class DocumentAssignmentView(APIView):
    def post(self, request, *args, **kwargs):
        client_id = request.data.get('clientId')
        if client_id:
            return Response({'message': 'Document assigned successfully!'}, status=status.HTTP_200_OK)
        return Response({'error': 'Client ID is required'}, status=status.HTTP_400_BAD_REQUEST)
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from .models import File

class FileDeleteView(APIView):
    def delete(self, request, client_id, file_id):
        file = get_object_or_404(File, client_id=client_id, id=file_id)
        file.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Comment
from .serializers import CommentSerializer
# views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Comment
from .serializers import CommentSerializer

# views.py
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Comment, Client
from .serializers import CommentSerializer

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Comment
from .serializers import CommentSerializer

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Comment
from .serializers import CommentSerializer

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

class ClientCommentView(APIView):
    def post(self, request, client_id):
        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(client_id=client_id)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Comment
from .serializers import CommentSerializer

class ClientCommentListView(APIView):
    def get(self, request, client_id):
        comments = Comment.objects.filter(client_id=client_id, parent=None)
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data)

    def post(self, request, client_id):
        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(client_id=client_id)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.http import Http404
from .models import Comment
from .serializers import CommentSerializer

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Comment
from .serializers import CommentSerializer

class ClientCommentListView(APIView):
    def get(self, request, client_id):
        comments = Comment.objects.filter(client_id=client_id, parent=None)
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data)

    def post(self, request, client_id):
        serializer = CommentSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save(client_id=client_id, user=request.user)  # Associer l'utilisateur actuel
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from .models import Comment
from .serializers import CommentSerializer

class ClientCommentDetailView(APIView):
    def get_object(self, comment_id):
        return get_object_or_404(Comment, id=comment_id)

    def get(self, request, comment_id):
        comment = self.get_object(comment_id)
        serializer = CommentSerializer(comment)
        return Response(serializer.data)

    def put(self, request, comment_id):
        comment = self.get_object(comment_id)
        serializer = CommentSerializer(comment, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, comment_id):
        comment = self.get_object(comment_id)
        comment.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Comment

class ClientCommentLikeView(APIView):
    def post(self, request, comment_id):
        comment = Comment.objects.get(id=comment_id)
        user = request.user
        if user in comment.liked_users.all():
            comment.liked_users.remove(user)
            comment.likes -= 1
            liked = False
        else:
            comment.liked_users.add(user)
            comment.likes += 1
            liked = True
        comment.save()
        return Response({'status': 'success', 'liked': liked, 'likes': comment.likes}, status=status.HTTP_200_OK)


