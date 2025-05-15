from django.db.models.signals import post_save
from django.dispatch import receiver
from account.models import User, Worker


@receiver(post_save, sender=User)
def create_worker_by_user(sender, instance: User, created: bool, **kwargs):
    """Сигнал для создания молели Сотрудника(Worker)"""
    if not created:
        return
    
    Worker.objects.create(user=instance)




