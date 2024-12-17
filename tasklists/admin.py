from django.contrib import admin
from .models import Tasklists


class TasklistsAdmin(admin.ModelAdmin):
    pass


admin.site.register(Tasklists, TasklistsAdmin)