def init_celery(celery, app):
    print(app.config)
    celery.conf.update(
        broker_url     = app.config['CELERY_BROKER_URL'],
        result_backend = app.config['CELERY_RESULT_BACKEND'],
        beat_schedule  = app.config['CELERY_BEAT_SCHEDULE'],
        namespace       = 'CELERY',
        task_serializer='json',
        accept_content=['json'],
        result_serializer='json',
        timezone='UTC',
        enable_utc=True,
        task_track_started=True,
        task_time_limit=30 * 60,
        worker_prefetch_multiplier=1,
        task_acks_late=True,
    )
    TaskBase = celery.Task
    class ContextTask(TaskBase):
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return TaskBase.__call__(self, *args, **kwargs)
    celery.Task = ContextTask