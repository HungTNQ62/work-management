from django.db import models

from users.models import User
from tasks.models import Tasks

# Create your models here.
class Comment(models.Model):
    comment = models.CharField(max_length=255, default="", blank=False, null=False)
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    task = models.ForeignKey(Tasks, on_delete=models.CASCADE)