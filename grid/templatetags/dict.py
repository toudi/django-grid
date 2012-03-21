from django.template import Library

register = Library()

def get(_dict, key):
    if type(_dict) == dict:
        if _dict.has_key(key):
            return _dict[key]
    else:
        if hasattr(_dict, key):
            return getattr(_dict, key)
    
    return None

def dict_contains(what, attribute):
    if type(what) == dict:
        return what.has_key(attribute)
    return False
    
def get_string_id(id):
    return str(id)

def getattr_filter(obj, attr):
    return getattr(obj, attr)
    
def check_order(val, col):
    if val==col or val=="-"+col:
        return True
    else:
        return False
        
def check_order_by(val):
    try:
        s = val.split("-")[1]
        return "background: url(/static/resources/images/toggle-collapse-dark.png) right no-repeat !important;"
    except:
        return "background: url(/static/resources/images/toggle-collapse-dark_asc.png) right no-repeat !important;"
    
register.filter("contains", dict_contains)
register.filter(get)
register.filter(check_order)
register.filter(check_order_by)
register.filter(get_string_id)
register.filter("getattr", getattr_filter)
