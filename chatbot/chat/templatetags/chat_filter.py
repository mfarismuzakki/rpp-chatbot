# Django
from django import template

register = template.Library()

@register.filter()
def message_summary(message):
    if len(message) > 26:
        message = message[0:26] + '...'

    return message
