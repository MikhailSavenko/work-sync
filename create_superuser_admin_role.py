import os
import django
import logging

logger = logging.getLogger(__name__)

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "work_sync.settings")
django.setup()

from django.contrib.auth import get_user_model
from django.db.utils import IntegrityError

from account.models import Worker

User = get_user_model()

EMAIL = os.getenv("DJANGO_SUPERUSER_EMAIL")

PASSWORD = os.getenv("DJANGO_SUPERUSER_PASSWORD")

if not User.objects.filter(email=EMAIL).exists():
    try:
        superuser = User.objects.create_superuser(email=EMAIL, password=PASSWORD)
        logger.info(f"Суперпользователь {superuser.email} создан.")

        superuser.worker.role = Worker.Role.ADMIN_TEAM
        superuser.worker.save()
        logger.info(f"Суперпользователь сотрудник изменена роль на админа команды {superuser.email}.")
    except IntegrityError as e:
        logger.warning(f"Суперпользователь {EMAIL} не был создан, возможно ошибка в данных. Error: {e}")
    except Exception as e:
        logger.warning(f"Суперпользователь {EMAIL} не был создан, непредвиденная ошибка. Error: {e}")
else:
    logger.warning(f"Суперпользователь c Email {EMAIL} уже существует")