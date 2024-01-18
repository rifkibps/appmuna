import json
from django.urls import reverse_lazy
from django.core.serializers.json import DjangoJSONEncoder

from django.db.models import Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from django.shortcuts import render
from django.views import View
from django.core import serializers

from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse, HttpResponse
from django.shortcuts import get_object_or_404

from . import models
from . import forms

class BackendAppClassView(View):

    def get(self, request):
        context = {
            'title' : 'Backend | Portal Administrator'
        }
        return render(request, 'backend/table_statistics/index.html', context)


# <======================================== UNIT CLASS VIEW ====================================================>

class BackendUnitsJsonClassView(LoginRequiredMixin, View):

    def post(self, request):
        
        data_wilayah = self._datatables(request)
        return HttpResponse(json.dumps(data_wilayah, cls=DjangoJSONEncoder), content_type='application/json')
		
    def _datatables(self, request):
        datatables = request.POST
        
        # Get Draw
        draw = int(datatables.get('draw'))
        start = int(datatables.get('start'))
        length = int(datatables.get('length'))
        page_number = int(start / length + 1)

        search = datatables.get('search[value]')

        order_idx = int(datatables.get('order[0][column]')) # Default 1st index for
        order_dir = datatables.get('order[0][dir]') # Descending or Ascending
        order_col = 'columns[' + str(order_idx) + '][data]'
        order_col_name = datatables.get(order_col)

        if (order_dir == "desc"):
            order_col_name =  str('-' + order_col_name)

        model = models.BackendUnitsModel.objects     
        model = model.exclude(Q(name=None))
      
        records_total = model.count()
        records_filtered = records_total
        
        if search:
            model = models.BackendUnitsModel.objects.filter(
                Q(name__icontains=search)|Q(desc__icontains=search)
            ).exclude(Q(name=None))

            records_total = model.count()
            records_filtered = records_total
        
        model = model.order_by(order_col_name)


        # Conf Paginator
        paginator = Paginator(model, length)

        try:
            object_list = paginator.page(page_number).object_list
        except PageNotAnInteger:
            object_list = paginator.page(1).object_list
        except EmptyPage:
            object_list = paginator.page(1).object_list

        
        data = []

        for idx, obj in enumerate(object_list):

            data.append(
            {
                'checkbox': f'<div class="form-check"><input type="checkbox" class="form-check-input" id="check{obj.id}"><label class="form-check-label" for="check{obj.id}">&nbsp;</label></div>',
                'no'    : idx+1,
                'name': obj.name,
                'desc': obj.desc,
                'actions': f'<a href="{reverse_lazy("backend:backend-units-input", kwargs={"unit_id": obj.id})}" class="action-icon"> <i class="mdi mdi-square-edit-outline"></i></a> <a href="javascript:void(0);" onclick="deleteUnit({obj.id})" class="action-icon"> <i class="mdi mdi-delete"></i></a>'
    
            })

        return {
            'draw': draw,
            'recordsTotal': records_total,
            'recordsFiltered': records_filtered,
            'data': data,
        }

class BackendUnitsClassView(View):

    def get(self, request):
        context = {
            'title' : 'Backend | Satuan Data',
            'data'  : models.BackendUnitsModel.objects.values()
        }

        return render(request, 'backend/table_statistics/units/units.html', context)

    # Delete method
    def post(self, request):

        is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'

        if is_ajax:
            if request.method == 'POST':
                
                id = request.POST.get('id')

                data = models.BackendUnitsModel.objects.filter(pk = id)

                if data.exists():
                    data.delete()
                    return JsonResponse({'status' : 'success', 'message': 'Data deleted successfully'})
                else:
                    return JsonResponse({'status': 'failed', 'message': 'Data not available'})
                
        return JsonResponse({'status': 'Invalid request'}, status=400)
    

class BackendUnitInputClassView(View):

    def get(self, request, *args, **kwargs):

        context = {
            'title' : 'Backend | Input Satuan Data',
            'form'  : forms.BackendUnitForm()
        }

        model = models.BackendUnitsModel.objects

        if self.kwargs.get('unit_id') is not None:
            if model.filter(pk=self.kwargs['unit_id']).exists:
                context['form'] = forms.BackendUnitForm(instance=model.get(pk=self.kwargs['unit_id']))

        return render(request, 'backend/table_statistics/units/input.html', context)


    def post(self, request, *args, **kwargs):

        is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'
        if is_ajax:
            if request.method == 'POST':

                if self.kwargs.get('unit_id') is not None:
                    data = get_object_or_404(models.BackendUnitsModel, pk=self.kwargs.get('unit_id'))
                    form = forms.BackendUnitForm(request.POST, instance=data)
                    msg = 'Data added successfully'
                else:
                    form = forms.BackendUnitForm(request.POST)
                    msg = 'Data updated successfully'

                if form.is_valid():
                    form.save()
                    return JsonResponse({"status": 'success', 'message': msg}, status=200)
                else:
                    return JsonResponse({"status": 'failed', "error": form.errors}, status=400)

        return JsonResponse({'status': 'Invalid request'}, status=400)
    


# <========================================== END BACKEND UNITS ===============================================>
    
class BackendPeriodsItemsClassView(View):
    def get(self, request):
        context = {
            'title' : 'Backend | Satuan Data'
        }
        return render(request, 'backend/table_statistics/periods.html', context)
    
class BackendRowsItemsClassView(View):
    def get(self, request):
        context = {
            'title' : 'Backend | Kelompok Baris'
        }
        return render(request, 'backend/table_statistics/rows.html', context)
    

class BackendCharsItemsClassView(View):
    def get(self, request):
        context = {
            'title' : 'Backend | Subjek'
        }
        return render(request, 'backend/table_statistics/subjects.html', context)


class BackendIndicatorsClassView(View):
    def get(self, request):
        context = {
            'title' : 'Backend | Tabel Statistik'
        }
        return render(request, 'backend/table_statistics/indicators.html', context)
    

class BackendContentIndicatorsClassView(View):
    def get(self, request):
        context = {
            'title' : 'Backend | Tabel Statistik'
        }
        return render(request, 'backend/table_statistics/content-tables.html', context)