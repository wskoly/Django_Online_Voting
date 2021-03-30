from django import template
register = template.Library()

@register.filter
def prg_bar(value, arg):
    if arg !=0:
        return round((value/arg)*100,2)
    else:
        return 0

@register.filter
def prg_cls(value,arg):
    if arg !=0:
        return int((value/arg)*100)
    else:
        return 0