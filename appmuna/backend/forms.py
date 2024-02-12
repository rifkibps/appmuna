from django import forms
from . import models

class BackendUnitForm(forms.ModelForm):

    class Meta:
        model = models.BackendUnitsModel

        fields = [
            'name',
            'desc',
        ]

        attrs_input = {
            'class' : 'form-control',
            'required': 'required',
            'placeholder': '...'
        }

        widgets = {
            'name': forms.TextInput(
                attrs = attrs_input | {'placeholder' : 'Isikan satuan'}
            ),
            'desc': forms.TextInput(
                attrs = attrs_input | {'placeholder' : 'Isikan keterangan satuan (opt)'}
            )
        }


class BackendPeriodForm(forms.ModelForm):

    class Meta:
        model = models.BackendPeriodsModel

        fields = [
            'name',
        ]

        attrs_input = {
            'class' : 'form-control',
            'required': 'required',
            'placeholder': '...'
        }

        widgets = {
            'name': forms.TextInput(
                attrs = attrs_input | {'placeholder' : 'Isikan periode data'}
            )
        }

class BackendRowForm(forms.ModelForm):

    class Meta:
        model = models.BackendRowsModel

        fields = [
            'name',
        ]

        attrs_input = {
            'class' : 'form-control',
            'required': 'required',
            'placeholder': '...'
        }

        widgets = {
            'name': forms.TextInput(
                attrs = attrs_input | {'placeholder' : 'Isikan judul baris'}
            )
        }


class BackendCharForm(forms.ModelForm):

    class Meta:
        model = models.BackendCharacteristicsModel

        fields = [
            'name',
        ]

        attrs_input = {
            'class' : 'form-control',
            'required': 'required',
            'placeholder': '...'
        }

        widgets = {
            'name': forms.TextInput(
                attrs = attrs_input | {'placeholder' : 'Isikan satuan'}
            )
        }


class BackendSubjectForm(forms.ModelForm):

    class Meta:
        model = models.BackendSubjectsModel

        fields = [
            'name',
            'subject_group',
            'show_state'
        ]

        attrs_input = { 
            'class' : 'form-control',
            'required': 'required',
            'placeholder': '...'
        }

        widgets = {
            'name': forms.TextInput(
                attrs = attrs_input | {'placeholder' : 'Isikan satuan'}
            ),
            'subject_group': forms.Select(
                attrs = attrs_input | {'class' : 'form-select', 'id': 'id_subject_group'}
            ),
            'show_state': forms.Select(
                 attrs = attrs_input | {'class' : 'form-select', 'id': 'id_show_state'}
            )
        }

class BackendIndicatorForm(forms.ModelForm):

    class Meta:
        model = models.BackendIndicatorsModel

        fields = [
            'subject_id',
            'subject_csa_id',
            'name',
            'desc',
            'footer_desc',
            'col_group_id',
            'row_group_id',
            'time_period_id',
            'time_period_id',
            'unit_id',
            'decimal_point',
            'stat_category',
            'level_data',
            'show_state',
        ]

        attrs_input = { 
            'class' : 'form-control',
            'required': 'required',
            'placeholder': '...'
        }

        widgets = {
            'subject_id': forms.Select(
                attrs = attrs_input | {'class' : 'form-select', 'id': 'subject_id_id'}
            ),
            'subject_csa_id': forms.Select(
                attrs = {'class' : 'form-select', 'id': 'subject_csa_id_id'}
            ),
            'name': forms.TextInput(
                attrs = attrs_input | {'placeholder' : 'Isikan nama indikator', 'id': 'name'}
            ),
            'desc': forms.TextInput(
                attrs = attrs_input | {'placeholder' : 'Isikan deskripsi', 'id': 'desc'}
            ),
            'footer_desc': forms.TextInput(
                attrs = attrs_input | {'placeholder' : 'Isikan keterangan / sumber data', 'id': 'footer_desc'}
            ),
            'col_group_id': forms.Select(
                attrs = {'class' : 'form-select', 'id': 'col_group_id_id'}
            ),
            'row_group_id': forms.Select(
                attrs = attrs_input | {'class' : 'form-select', 'id': 'row_group_id_id'}
            ),
            'time_period_id': forms.Select(
                attrs = attrs_input | {'class' : 'form-select', 'id': 'time_period_id_id'}
            ),
            'unit_id': forms.Select(
                attrs = attrs_input | {'class' : 'form-select', 'id': 'unit_id_id'}
            ),
            'decimal_point': forms.TextInput(
                attrs = attrs_input  | {'id': 'decimal_point'}
            ),
            'stat_category': forms.Select(
                attrs = attrs_input | {'class' : 'form-select', 'id': 'stat_category'}
            ),
            'level_data': forms.Select(
                attrs = attrs_input | {'class' : 'form-select', 'id': 'level_data'}
            ),
            'show_state': forms.Select(
                attrs = attrs_input | {'class' : 'form-select', 'id': 'show_state'}
            )
        }


class BackendContentStatisForm(forms.ModelForm):

    class Meta:
        model = models.BackendContentStatisModel

        fields = [
            'subject_id',
            'subject_csa_id',
            'title',
            'year',
            'content',
            'footer_desc',
            'stat_category',
            'show_state',
        ]

        attrs_input = {
            'class' : 'form-control',
            'required': 'required',
            'placeholder': '...'
        }

        widgets = {
            'subject_id': forms.Select(
                attrs = attrs_input | {'class' : 'form-select', 'id' : 'subject_id'}
            ),
            'subject_csa_id': forms.Select(
                attrs = {'class' : 'form-select' , 'id' : 'subject_csa_id'}
            ),
            'title': forms.TextInput(
                attrs = attrs_input | {'placeholder' : 'Tuliskan judul berita statistik', 'id' : 'title'}
            ),
            'year': forms.TextInput(
                attrs = attrs_input | {'placeholder' : 'Tuliskan keterangan tahun', 'id' : 'year'}
            ),
            'content': forms.TextInput(
                attrs = attrs_input  | {'id' : 'content'}
            ),
            'footer_desc': forms.TextInput(
                attrs = attrs_input  | {'placeholder' : 'Tuliskan keterangan sumber/informasi lain', 'id' : 'footer_desc'}
            ),
            'stat_category': forms.Select(
                attrs = attrs_input | {'class' : 'form-select', 'id' : 'stat_category'}
            ),
            'show_state': forms.Select(
                attrs = attrs_input | {'class' : 'form-select', 'id' : 'show_state'}
            )
        }


class BackendStatsNewsForm(forms.ModelForm):

    class Meta:
        model = models.BackendStatsNewsModel

        fields = [
            'subject_id',
            'subject_csa_id',
            'title',
            'author',
            'content',
            'file',
            'thumbnail',
            'show_state',
        ]

        attrs_input = {
            'class' : 'form-control',
            'required': 'required',
            'placeholder': '...'
        }

        widgets = {
            'subject_id': forms.Select(
                attrs = attrs_input | {'class' : 'form-select', 'id' : 'subject_id'}
            ),
            'subject_csa_id': forms.Select(
                attrs = {'class' : 'form-select' , 'id' : 'subject_csa_id'}
            ),
            'title': forms.TextInput(
                attrs = attrs_input | {'placeholder' : 'Tuliskan judul berita statistik', 'id' : 'title'}
            ),
            'author': forms.TextInput(
                attrs = attrs_input | {'id' : 'author'}
            ),
            'content': forms.TextInput(
                attrs = attrs_input  | {'id' : 'content'}
            ),
            'file': forms.FileInput(
                attrs = attrs_input | {'id' : 'file'}
            ),
            'thumbnail': forms.FileInput(
                attrs = attrs_input   | {'id' : 'thumbnail'}
            ),
            'show_state': forms.Select(
                attrs = attrs_input | {'class' : 'form-select', 'id' : 'show_state'}
            )
        }


class BackendInfographicForm(forms.ModelForm):

    class Meta:
        model = models.BackendInfographicsModel

        fields = [
            'subject_id',
            'subject_csa_id',
            'title',
            'desc',
            'file',
            'show_state',
        ]

        attrs_input = {
            'class' : 'form-control',
            'required': 'required',
            'placeholder': '...'
        }

        widgets = {
            'subject_id': forms.Select(
                attrs = attrs_input | {'class' : 'form-select',  'id' : 'subject_id'}
            ),
            'subject_csa_id': forms.Select(
                attrs = {'class' : 'form-select' , 'id' : 'subject_csa_id'}
            ),
            'title': forms.TextInput(
                attrs = attrs_input | {'placeholder' : 'Tuliskan judul infogragis', 'id' : 'title'}
            ),
            'desc': forms.TextInput(
                attrs = attrs_input  | {'id' : 'desc'}
            ),
            'file': forms.FileInput(
                attrs = attrs_input | {'id' : 'file'}
            ),
            'show_state': forms.Select(
                attrs = attrs_input | {'class' : 'form-select', 'id' : 'show_state'}
            )
        }


class BackendVideoGraphicForm(forms.ModelForm):

    class Meta:
        model = models.BackendVideoGraphicsModel

        fields = [
            'subject_id',
            'subject_csa_id',
            'title',
            'desc',
            'link',
            'file',
            'thumbnail',
            'show_state',
        ]

        attrs_input = {
            'class' : 'form-control',
            'required': 'required',
            'placeholder': '...'
        }

        widgets = {
            'subject_id': forms.Select(
                attrs = attrs_input | {'class' : 'form-select', 'id' : 'subject_id'}
            ),
            'subject_csa_id': forms.Select(
                attrs = {'class' : 'form-select' , 'id' : 'subject_csa_id'}
            ),
            'title': forms.TextInput(
                attrs = attrs_input | {'placeholder' : 'Tuliskan judul berita statistik', 'id' : 'title'}
            ),
            'desc': forms.TextInput(
                attrs = attrs_input  | {'id' : 'desc'}
            ),
            'link': forms.TextInput(
                attrs = {'class' : 'form-control', 'placeholder' : 'Paste link Youtube Videografis', 'id' : 'link'}
            ),
            'file': forms.FileInput(
                attrs = {'class' : 'form-control' , 'id' : 'file'}
            ),
            'thumbnail': forms.FileInput(
                attrs = attrs_input   | {'id' : 'thumbnail'}
            ),
            'show_state': forms.Select(
                attrs = attrs_input | {'class' : 'form-select', 'id' : 'show_state'}
            )
        }
    

class BackendDataRequestsForm(forms.ModelForm):

    class Meta:
        model = models.BackendDataRequestsModel


        fields = [
            'name_person',
            'contact_person',
            'agency_person',
            'subject_request',
            'desc_data',
            'app_letter',
            'show_state',
        ]

        attrs_input = {
            'class' : 'form-control',
            'required': 'required',
            'placeholder': '...'
        }

        widgets = {
            'name_person': forms.TextInput(
                attrs = attrs_input | {'id' : 'name_person'}
            ),
            'contact_person': forms.TextInput(
                attrs = attrs_input | {'id' : 'contact_person'}
            ),
            'agency_person': forms.TextInput(
                attrs = attrs_input | {'id' : 'agency_person'}
            ),
            'subject_request': forms.TextInput(
                attrs = attrs_input | {'placeholder' : 'Tuliskan judul berita statistik', 'id' : 'subject_request'}
            ),
            'desc_data': forms.TextInput(
                attrs = attrs_input | {'placeholder' : 'Tuliskan judul berita statistik', 'id' : 'desc_data'}
            ),
            'app_letter': forms.FileInput(
                attrs = {'class' : 'form-control' , 'id' : 'app_letter'}
            ),
            'show_state': forms.Select(
                attrs = attrs_input | {'class' : 'form-select', 'id' : 'show_state'}
            )
        }


class BackendPublicationsForm(forms.ModelForm):

    class Meta:
        model = models.BackendPublicationsModel

        fields = [
            'title',
            'catalog_no',
            'publication_no',
            'issn',
            'release',
            'abstract',
            'file',
            'show_state',
        ]

        attrs_input = {
            'class' : 'form-control',
            'required': 'required',
            'placeholder': '...'
        }

        widgets = {
            'title': forms.TextInput(
                attrs = attrs_input | {'id' : 'title'}
            ),
            'catalog_no': forms.TextInput(
                attrs = attrs_input | {'id' : 'catalog_no'}
            ),
            'publication_no': forms.TextInput(
                attrs = attrs_input | {'id' : 'publication_no'}
            ),
            'issn': forms.TextInput(
                attrs =  {'class' : 'form-control' , 'id' : 'issn'}
            ),
            'release': forms.DateInput(
                attrs = attrs_input | {'id' : 'release'}
            ),
            'abstract': forms.TextInput(
                attrs = attrs_input | {'id' : 'abstract'}
            ),
            'file': forms.FileInput(
                attrs = attrs_input | {'id' : 'file'}
            ),
            'show_state': forms.Select(
                attrs = attrs_input | {'class' : 'form-select', 'id' : 'show_state'}
            )
        }