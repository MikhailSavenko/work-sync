import factory
from factory.django import DjangoModelFactory
from django.contrib.auth import get_user_model
from datetime import datetime, timezone

from account.models import Team
from task.models import Task

User = get_user_model()


class UserFactory(DjangoModelFactory):
    class Meta:
        model = User
    
    email = factory.Sequence(lambda n: "user%d@example.com" %n)


class TeamFactory(DjangoModelFactory):
    class Meta:
        model = Team
    
    title = factory.Sequence(lambda n: "team%d" %n)


class TaskDeadlineFactory(DjangoModelFactory):
    class Meta:
        model = Task
    
    title = factory.Sequence(lambda n: "task%d" %n)
    description = factory.Sequence(lambda n: "description%d" %n)
    deadline = datetime(2025, 12, 31, 23, 59, 59, tzinfo=timezone.utc)


# class TaskFactory(DjangoModelFactory):
#     class Meta:
#         model = Task
    
#     title = factory.Sequence(lambda n: "task%d" %n)