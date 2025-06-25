import logging

from django.db.models.signals import post_save
from django.dispatch import receiver

from account.models import User, Worker

logger = logging.getLogger(__name__)


@receiver(post_save, sender=User)
def create_worker_by_user(sender, instance: User, created: bool, **kwargs):
    """Сигнал для создания молели Сотрудника(Worker)"""
    if not created:
        return
    logger.info(f"Сигнал 'create_worker_by_user' был вызван для User {instance.id}.")
    try:
        Worker.objects.create(user=instance)
        logger.info(f"Успешное создание Worker для User {instance.id}")
    except Exception as e:
        logger.error(f"Worker не был создан для User {instance.id}. Ошибка: {e}", exc_info=True)
