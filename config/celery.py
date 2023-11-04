from __future__ import absolute_import, unicode_literals
import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

app = Celery('config')

# Использование строки здесь означает, что работник не должен сериализовать
# объект конфигурации для дочерних процессов.
# - namespace='CELERY' означает, что все связанные с celery настройки
#   должны быть префиксом `CELERY_` в файле settings.py
app.config_from_object('django.conf:settings', namespace='CELERY')

# Загрузка задач модулей из всех зарегистрированных приложений Django.
app.autodiscover_tasks()
