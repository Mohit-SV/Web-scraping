from flask import Flask


app = Flask(__name__)

from . import views

# celery -A reuters_assist.config.celery worker -l info
# celery -A reuters_assist.config.celery beat -l info
