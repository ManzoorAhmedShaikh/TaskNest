from django.db import models
from django.contrib.auth.models import User
from datetime import datetime

class Notes(models.Model):
    username = models.ForeignKey(User, on_delete=models.CASCADE)
    note_name = models.CharField(max_length=60)
    note_status = models.BooleanField()
    note_date = models.DateTimeField(default=datetime.now)