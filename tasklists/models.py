from django.db import models

from users.models import User
from workboards.models import Workboards

# Create your models here.
class Tasklists(models.Model):
    name = models.CharField(max_length=255, default="", blank=False, null=False)
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    workboard = models.ForeignKey(Workboards, on_delete=models.CASCADE)
