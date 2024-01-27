from django import template

register = template.Library()

@register.filter
def get_item(list_data, item):
    
    data = []
    for dt in list_data:
        if  dt.get(str(item)) is not None:
            data.append(dt.get(str(item)))

    return data



