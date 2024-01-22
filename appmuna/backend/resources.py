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
        