from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta
from django.core.mail import send_mail
from machines.models import Machine  # Assurez-vous que le modèle Machine est importé correctement
from machines.tasks import send_machine_reminder_email  # Importez la tâche Celery

class Command(BaseCommand):
    help = 'Send reminder emails for machines that require intervention'

    def handle(self, *args, **kwargs):
        # Obtenez l'heure actuelle
        now = timezone.now()

        # Calculez la date de rappel (2 minutes avant l'heure actuelle)
        reminder_date = now - timedelta(minutes=2)

        # Recherchez les machines qui ont été créées il y a plus de 2 minutes et qui n'ont pas encore reçu de rappel
        machines = Machine.objects.filter(date_installation__lte=reminder_date, reminder_sent=False)

        for machine in machines:
            # Déclenchement de la tâche Celery pour envoyer un email de rappel
            send_machine_reminder_email.delay(machine.id_machine)

            # Marquez le rappel comme envoyé pour cette machine
            machine.reminder_sent = True
            machine.save()

        # Affichez un message de succès dans la console
        self.stdout.write(self.style.SUCCESS('Successfully sent reminders for machines'))