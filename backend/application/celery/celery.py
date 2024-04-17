from celery import Celery
from flask import current_app as app
from celery.beat import EmbeddedService, ScheduleEntry
from celery.schedules import crontab

celery = Celery(
    "LibraryVue",
    broker=app.config["CELERY_BROKER_URL"],
    backend=app.config["CELERY_RESULT_BACKEND"],
    include=["application.celery.tasks"],
    broker_connection_retry_on_startup=True,
)


class ContextTask(celery.Task):
    def __call__(self, *args, **kwargs):
        with app.app_context():
            return self.run(*args, **kwargs)


celery.Task = ContextTask
