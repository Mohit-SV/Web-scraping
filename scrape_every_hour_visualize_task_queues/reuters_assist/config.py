from pymongo import MongoClient
from celery import Celery
from datetime import timedelta
from . import app


def make_celery(app):
    celery = Celery(
        app.import_name,
        backend=app.config['CELERY_RESULT_BACKEND'],
        broker=app.config['CELERY_BROKER_URL']
    )
    celery.conf.update(app.config)

    class ContextTask(celery.Task):
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return self.run(*args, **kwargs)

    celery.Task = ContextTask
    return celery


app.config.update(
    CELERY_BROKER_URL='redis://localhost:6379',
    CELERY_RESULT_BACKEND='redis://localhost:6379',
    # CELERY_TASK_SERIALIZER='pickle',
    # CELERY_RESULT_SERIALIZER = 'pickle',
    # CELERY_ACCEPT_CONTENT = ['pickle'],
    CELERYBEAT_SCHEDULE={
        'insert-news-every-10s': {
            'task': 'beat_news.tasks.scra_per',
            'schedule': timedelta(seconds=40)
        },
        'infer-news-schema-every-10s': {
            'task': 'beat_news.tasks.infer_schema',
            'schedule': timedelta(seconds=20)
        },
    }
)
celery = make_celery(app)

user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 ' \
             '(KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'

client = MongoClient("localhost", 27017)

