from django.template import Library

register = Library()

def page(qdict, value):
    newd = qdict.copy()
    newd["page"] = value
    return newd.urlencode()
    
register.filter(page)