import factory
from factory.django import DjangoModelFactory
from django.contrib.auth import get_user_model

from account.models import Team
from event.models import Meeting
from task.models import Evaluation, Task

User = get_user_model()


class UserFactory(DjangoModelFactory):
    class Meta:
        model = User
    
    email = factory.Sequence(lambda n: "user%d@example.com" %n)


class TeamFactory(DjangoModelFactory):
    class Meta:
        model = Team
    
    title = factory.Sequence(lambda n: "team%d" %n)


class TaskFactory(DjangoModelFactory):
    class Meta:
        model = Task
    
    title = factory.Sequence(lambda n: "task%d" %n)
    description = factory.Sequence(lambda n: "description%d" %n)


class MeetingFactory(DjangoModelFactory):
    class Meta:
        model = Meeting
    
    description = factory.Sequence(lambda n: "description%d" %n)


class EvaluationFactory(DjangoModelFactory):
    class Meta:
        model = Evaluation
    
    score = 5


    

    