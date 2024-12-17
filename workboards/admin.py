from django.contrib import admin
from .models import Workboards


class WorkboardsAdmin(admin.ModelAdmin):
    pass


admin.site.register(Workboards, WorkboardsAdmin)