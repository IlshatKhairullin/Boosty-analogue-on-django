from random import randrange
from django import template

register = template.Library()


@register.inclusion_tag("web/tags/filter_link.html")
def filter_link(title, url_part, query_params):
    is_active = url_part in query_params
    if not url_part:
        is_active = len(query_params) == 0
    return {"title": title, "url_part": url_part, "is_active": is_active}


@register.filter(name="addclass")
def addclass(value, arg):
    return value.as_widget(attrs={"class": arg})


@register.filter(name="random_id")
def random_id(range2: int) -> int:
    return randrange(range2)
