import os
from celery import Celery

# Définir le module de paramètres par défaut pour 'celery'
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Xerox.settings')

app = Celery('Xerox')

# Utiliser une chaîne pour le nom du module des tâches.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Charger les tâches des modules installés
app.autodiscover_tasks()

@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')
