import factory
from factory.django import DjangoModelFactory
from django.contrib.auth import get_user_model

from account.models import Team

User = get_user_model()


class UserFactory(DjangoModelFactory):
    class Meta:
        model = User
    
    email = factory.Sequence(lambda n: "user%d@example.com" %n)


class TeamFactory(DjangoModelFactory):
    class Meta:
        model = Team
    
    title = factory.Sequence(lambda n: "team%d@example.com" %n)
    