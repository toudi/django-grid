from django.template import Library

register = Library()

def limit(_list, howmany):
    return _list[:howmany]
    
register.filter(limit)
