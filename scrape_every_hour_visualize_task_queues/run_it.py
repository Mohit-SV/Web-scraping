from reuters_assist import app

app.run(port=5000, debug=True)

# celery -A reuters_assist.config.celery worker -l info
# celery -A reuters_assist.config.celery beat -l info
