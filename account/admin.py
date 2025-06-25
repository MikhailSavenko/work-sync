from django.contrib import admin

from account.models import Team, User, Worker

admin.site.register(User)
admin.site.register(Worker)
admin.site.register(Team)
