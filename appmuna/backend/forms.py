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