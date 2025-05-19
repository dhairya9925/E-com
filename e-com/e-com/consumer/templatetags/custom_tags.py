# dinosoar/dinofacts/templatetags/dinotags.py

from django import template
from types import SimpleNamespace
from core.models import Orders
from datetime import datetime

register = template.Library()

# class Dictionary:
#     def __init__(self, dict):
#         print(dict)
#         self.__dict__.update(dict)


@register.filter
def make_obj(dict):
    obj = SimpleNamespace(**dict)
    # obj = Dictionary(dict)
    return obj
