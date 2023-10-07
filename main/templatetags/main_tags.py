from django import template
from django.db.models import Count

from main.models import CustomUser

register = template.Library()

@register.simple_tag(name='all_user')
def all_user():
    return CustomUser.objects.all()


@register.filter(name="slice_email")
def slice_email(value, arg):
    """Removes email`s name from the given string"""
    email = value.split('@')[0]
    return email
