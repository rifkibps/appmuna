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
            'unit_id',
            'decimal_point',
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
            'show_state': forms.Select(
                attrs = attrs_input | {'class' : 'form-select', 'id': 'show_state'}
            )
        }
