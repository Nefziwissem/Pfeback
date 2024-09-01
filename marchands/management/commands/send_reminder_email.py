from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta
from marchands.models import Marchand  # Assurez-vous que le modèle Marchand est importé correctement
from marchands.tasks import send_reminder_email  # Importez la tâche Celery

class Command(BaseCommand):
    help = 'Send reminder emails for marchands that require intervention'

    def handle(self, *args, **kwargs):
        # Obtenez l'heure actuelle
        now = timezone.now()

        # Calculez la date de rappel (2 minutes avant l'heure actuelle)
        reminder_date = now - timedelta(minutes=2)

        # Recherchez les marchands qui ont été créées il y a plus de 2 minutes et qui n'ont pas encore reçu de rappel
        marchands = Marchand.objects.filter(date_installation__lte=reminder_date, reminder_sent=False)

        for marchand in marchands:
            # Déclenchement de la tâche Celery pour envoyer un email de rappel
            send_reminder_email.delay(marchand.id_marchand)

            # Marquez le rappel comme envoyé pour cette marchand
            marchand.reminder_sent = True
            marchand.save()

        # Affichez un message de succès dans la console
        self.stdout.write(self.style.SUCCESS('Successfully sent reminders for marchands'))