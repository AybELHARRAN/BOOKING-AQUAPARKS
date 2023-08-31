from django import template
register= template.Library()

#! filters
@register.filter
def get(List, index):
    return List[index]