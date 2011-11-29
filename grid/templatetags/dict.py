from django.template import Library

register = Library()

def get(dict, key):
    if type(dict) == dict:
        if dict.has_key(key):
            return dict[key]
    else:
        if hasattr(dict, key):
            return getattr(dict, key)
    
    return None

register.filter(get)
