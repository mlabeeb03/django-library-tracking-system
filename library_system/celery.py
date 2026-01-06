import os
from celery import Celery
from celery.schedules import crontab
# from library import tasks

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'library_system.settings')

app = Celery('library_system')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

# @app.on_after_configure.connect
# def setup_periodic_tasks(sender: Celery, **kwargs):
#     sender.add_periodic_task(
#         crontab(hour=7, minute=30, day_of_week=1),
#         tasks.check_overdue_loans.s(),
#     )