from pathlib import Path
from pkgutil import iter_modules

from celery import Celery

from core.celery_beat_schedule import CELERY_BEAT_SCHEDULE
from core.config import settings


def find_task_modules():
    api_path = [f"{Path().absolute()}/app"]
    return [module.name for module in iter_modules(api_path, prefix="app.")]


celery = Celery(
    __name__, broker=settings.CELERY_BROKER, backend=settings.CELERY_BACKEND
)
celery.autodiscover_tasks(find_task_modules())
celery.conf.beat_schedule = CELERY_BEAT_SCHEDULE
celery.conf.timezone = "UTC"


@celery.task(bind=True)
def debug_task(self):
    print("Debug task is running...")
