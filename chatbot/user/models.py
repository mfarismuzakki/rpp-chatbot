from django.db import models
from core.models import Template

class User(Template, models.Model):
    username = models.TextField(max_length=255)
