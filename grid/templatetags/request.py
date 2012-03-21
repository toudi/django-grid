from django.template import Library

register = Library()

def order(qdict, value):
    newd = qdict.copy()
    newd["order"] = value
    return newd.urlencode()

def page(qdict, value):
    newd = qdict.copy()
    newd["page"] = value
    return newd.urlencode()
    
register.filter(page)
register.filter(order)