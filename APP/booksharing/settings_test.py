from booksharing.settings import * # noqa

DEBUG = False
CELERY_BROKER_URL = 'memory://localhost/'
EMAIL_BACKEND = 'django.core.mail.outbox'
CELERY_TASK_ALWAYS_EAGER = True
