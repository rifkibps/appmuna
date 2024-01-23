from import_export import resources, widgets

from import_export.fields import Field
from . import models

class BackendUnitsResource(resources.ModelResource):

    name = Field(attribute="name", column_name="Nama Satuan")
    desc = Field(attribute="desc", column_name="Keterangan Satuan")

    class Meta:
        model = models.BackendUnitsModel
        fields = (
            'name',
            'desc',
        )
        

class BackendPeriodsResource(resources.ModelResource):

    period_id__name = Field(attribute="period_id__name", column_name="Periode Data")
    item_period = Field(attribute="item_period", column_name="Item Periode")

    class Meta:
        model = models.BackendPeriodNameItemsModel
        fields = (
            'period_id__name',
            'item_period',
        )
        

class BackendRowsResource(resources.ModelResource):

    row_id__name = Field(attribute="row_id__name", column_name="Nama Judul")
    order_num = Field(attribute="order_num", column_name="Urutan Item")
    item_row = Field(attribute="item_row", column_name="Item Judul Baris")

    class Meta:
        model = models.BackendRowsItemsModel
        fields = (
            'row_id__name',
            'order_num',
            'item_row'
        )
        