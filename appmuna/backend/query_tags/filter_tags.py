from django import template
from backend import models

register = template.Library()

@register.filter
def get_item(list_data, item):
    
    data = []
    for dt in list_data:
        if  dt.get(str(item)) is not None:
            data.append(dt.get(str(item)))

    return data

@register.filter
def get_item_row_name(row_item_id, field_name):
    model = models.BackendRowsItemsModel.objects.filter(pk = row_item_id).values().first()
    return model[field_name]


@register.filter
def get_item_col_name(col_item_id, field_name):
    model = models.BackendCharacteristicItemsModel.objects.filter(pk = col_item_id).values().first()
    return model[field_name]