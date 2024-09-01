# machines/tasks.py
from celery import shared_task
from django.core.mail import send_mail
from .models import Machine

@shared_task(name='machines.send_reminder_email')
def send_machine_reminder_email(machine_id):
    try:
        machine = Machine.objects.get(id_machine=machine_id)
        send_mail(
            'Reminder: Intervention Needed',
            f'The machine {machine.nom_machine} needs an intervention.',
            'wissrm134@gmail.com',  # FROM email
            ['wissrm134@gmail.com'],  # TO email
            fail_silently=False,
        )
    except Machine.DoesNotExist:
        print(f"Machine with ID {machine_id} does not exist.")
