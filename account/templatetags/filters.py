from django import template

register = template.Library()

@register.filter()
def ranges(count=21):
    return range(1, count)
