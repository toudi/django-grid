from django.template import Library

register = Library()

def get_verbose_name(meta, field):
    return meta.get_field(field).verbose_name
    
register.filter(get_verbose_name)