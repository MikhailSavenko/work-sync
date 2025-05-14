from django.contrib import admin
from task.models import Task, Evaluation, Comment


admin.site.register(Task)
admin.site.register(Evaluation)
admin.site.register(Comment)