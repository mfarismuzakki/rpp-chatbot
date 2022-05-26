from random import choices
from django.db import models
from core.models import Template
from user.models import User


class Chat(Template, models.Model):
    sender = models.ForeignKey(User,
        on_delete=models.CASCADE,
        related_name='sender')
    recipient = models.ForeignKey(User,
        on_delete=models.CASCADE,
        related_name='recipient')
    message = models.TextField(null=True, blank=True)
