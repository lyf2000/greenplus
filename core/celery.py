import os
from datetime import timedelta

from celery import Celery

# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')

app = Celery('core')

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django app configs.
app.autodiscover_tasks()

app.conf.beat_schedule = {
    # 'send-report-every-single-minute': {
    #     'task': 'app1.tasks.send_verification_email',
    #     'schedule': timedelta(seconds=5),  # change to `crontab(minute=0, hour=0)` if you want it to run daily at midnight
    # },
}

app.conf.update(
    task_serializer='json',
    accept_content=['json'],  # Ignore other content
    result_serializer='json',
    result_expires = timedelta(seconds=15),
    result_persistent = True,
    # task_routes = {
    #     'app1.tasks.send_verification_email': {'queue': 'send'},
    # },
)


@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))
