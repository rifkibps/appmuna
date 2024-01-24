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
        

class BackendSubjectResource(resources.ModelResource):

    name = Field(attribute="name", column_name="Nama Subject")
    subject_group = Field(attribute="get_subject_group_display", column_name="Kelompok Subject")
    show_state = Field(attribute="get_show_state_display", column_name="Tampilkan Subject")

    class Meta:
        model = models.BackendSubjectsModel
        fields = (
            'name',
            'subject_group',
            'show_state'
        )
        

class BackendIndicatorResource(resources.ModelResource):

    subject_id = Field(attribute="subject_id__name", column_name="Subjek Statistik")
    subject_csa_id = Field(attribute="subject_csa_id__name", column_name="Subjek Statistik CSA")
    name = Field(attribute="name", column_name="Nama Indikator")
    desc = Field(attribute="desc", column_name="Deskripsi Indikator")
    footer_desc = Field(attribute="footer_desc", column_name="Keterangan Indikator")
    col_group_id = Field(attribute="col_group_id__name", column_name="Kelompok Karakteristik")
    row_group_id = Field(attribute="row_group_id__name", column_name="Kelompok Judul Baris")
    time_period_id = Field(attribute="time_period_id__name", column_name="Periode Waktu")
    unit_id = Field(attribute="unit_id__name", column_name="Satuan Data")
    decimal_point = Field(attribute="decimal_point", column_name="Jumlah Desimal")
    stat_category = Field(attribute="get_stat_category_display", column_name="Kategori Statistik")
    show_state = Field(attribute="get_show_state_display", column_name="Tampilkan Indikator")
    created_at = Field(attribute="created_at", column_name="Dibuat")
    updated_at = Field(attribute="updated_at", column_name="Terakhir Diupdate")

    class Meta:
        model = models.BackendIndicatorsModel
        fields = (
            'subject_id',
            'subject_csa_id',
            'name',
            'desc',
            'footer_desc',
            'col_group_id',
            'row_group_id',
            'time_period_id',
            'unit_id',
            'decimal_point',
            'stat_category',
            'show_state',
            'created_at',
            'updated_at',
        )
        