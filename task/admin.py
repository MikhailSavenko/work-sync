from django.contrib import admin

from task.models import Comment, Evaluation, Task

admin.site.register(Task)
admin.site.register(Evaluation)
admin.site.register(Comment)
