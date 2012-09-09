from django import template

register = template.Library()

#count of queryset
def count(value):
    return value.count()
register.filter('count',count)
