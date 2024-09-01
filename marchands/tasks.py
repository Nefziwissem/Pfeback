from celery import shared_task
from django.core.mail import send_mail
from .models import Marchand

from celery import shared_task

@shared_task(name='marchands.send_reminder_email')
def send_reminder_ematil(marchand_id):
    try:
        marchand = Marchand.objects.get(id_marchand=marchand_id)
        send_mail(
            'Reminder: Action Required',
            f'Dear {marchand.nom_marchand},\n\nThis is a reminder for the action required.',
            'samaraouadi7@gmail.com',  # FROM email
            [marchand.email],
            fail_silently=False,
        )
        
        # Optionnel : Réinitialiser la date de rappel si nécessaire
        marchand. date_entretien = None
        marchand.save()
    except Marchand.DoesNotExist:
        print(f"Marchand with id {marchand_id} does not exist.")
    except Exception as e:
        print(f"Failed to send email to {marchand.email}: {e}")
