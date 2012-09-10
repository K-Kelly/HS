from django import template

register = template.Library()

#count of queryset
def count(value):
    return value.count()
register.filter('count',count)

def to_height(value):
    dictionary = {66:"5'6",67:"5'7",68:"5'8",69:"5'9",70:"5'10",71:"5'11",72:"6'0",73:"6'1",74:"6'2",75:"6'3",76:"6'4",77:"6'5",78:"6'6",79:"6'7",80:"6'8",81:"6'9",82:"6'10",83:"6'11"}
    return dictionary[value]
register.filter('to_height',to_height)
