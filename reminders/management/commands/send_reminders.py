from django.core.management.base import BaseCommand
from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta
from django.core.mail import send_mail
from Client.models import Client

class Command(BaseCommand):
    help = 'Send reminder emails to clients'

    def handle(self, *args, **kwargs):
        now = timezone.now()
        reminder_date = now - timedelta(minutes=2)
        clients = Client.objects.filter(created_at__lte=reminder_date, reminder_sent=False)

        for client in clients:
            send_mail(
                'Reminder',
                f'Dear {client.name}, this is a reminder about your account.',
                'samaraouadi7@gmail.com',  # Replace with your email address
                [client.email],
                fail_silently=False,
            )
            client.reminder_sent = True
            client.save()

        self.stdout.write(self.style.SUCCESS('Successfully sent reminders to clients'))
