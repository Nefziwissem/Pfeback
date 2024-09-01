from celery import shared_task
from django.core.mail import send_mail
from .models import Client

@shared_task
def send_reminder_email(client_id):
    try:
        client = Client.objects.get(id=client_id)
        send_mail(
            'Reminder: Payment Due',
            f'Dear {client.name},\n\nYou have an outstanding amount of {client.amount_remaining}. Please make the payment at your earliest convenience.',
            'samaraouadi7@gmail.com',
            [client.email],
            fail_silently=False,
        )
        
        client.reminder_date = None
        client.save()
    except Client.DoesNotExist:
        print(f"Client with id {client_id} does not exist.")
    except Exception as e:
        print(f"Failed to send email to {client.email}: {e}")
