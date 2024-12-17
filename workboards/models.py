from django.db import models

from users.models import User

# Create your models here.

class Workboards(models.Model):
    name = models.CharField(max_length=255, default="", blank=False, null=False)
    creator = models.ForeignKey(User, on_delete=models.CASCADE)

