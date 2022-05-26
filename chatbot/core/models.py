from datetime import datetime
from django.db import models


class Template(models.Model):
    status = models.BooleanField(default=True) 
    create_dt = models.DateTimeField(default=datetime.now) 

    class Meta:
        abstract = True