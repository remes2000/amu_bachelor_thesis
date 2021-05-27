from urllib.parse import urlencode
from django import template

from amu_bachelor_thesis_app.models import Thesis, Lecturer, ThesisProposition

register = template.Library()


@register.simple_tag
def count_taken_thesis(lecturer):
    return Thesis.objects.filter(lecturer=lecturer).exclude(student_id=None).count()


@register.simple_tag
def count_not_taken_thesis(lecturer):
    return Thesis.objects.filter(lecturer=lecturer, student_id=None).count()


@register.simple_tag
def count_thesis(lecturer):
    return Thesis.objects.filter(lecturer=lecturer).count()


@register.simple_tag
def count_thesis_propositions(lecturer):
    return ThesisProposition.objects.filter(lecturer=lecturer, is_active=True).count()
