from celery.schedules import crontab

CELERY_BEAT_SCHEDULE = {
    # "trigger_test_task": {
    #     "task": "core.celery.debug_task",
    #     # Run at every minute
    #     "schedule": crontab(minute="*/1"),
    # },
}
