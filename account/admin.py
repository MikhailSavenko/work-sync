from django.contrib import admin
from account.models import User, Worker, Team


admin.site.register(User)
admin.site.register(Worker)
admin.site.register(Team)
