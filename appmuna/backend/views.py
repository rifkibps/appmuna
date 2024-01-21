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

from . import models, forms, resources
from operator import itemgetter

class BackendAppClassView(LoginRequiredMixin, View):

    def get(self, request):
        context = {
            'title' : 'Backend | Portal Administrator'
        }
        return render(request, 'backend/table_statistics/index.html', context)


# <======================================== START BACKEND UNITS ====================================================>

class BackendUnitsJsonClassView(LoginRequiredMixin, View):

    def post(self, request):
        
        data = self._datatables(request)
        return HttpResponse(json.dumps(data, cls=DjangoJSONEncoder), content_type='application/json')
		
    def _datatables(self, request):

        # Define default column for ordering first request
        def_col = 'name' 

        datatables = request.POST
        # Get Draw
        draw = int(datatables.get('draw'))
        start = int(datatables.get('start'))
        search = datatables.get('search[value]')

        order_idx = int(datatables.get('order[0][column]')) # Default 1st index for
        order_dir = datatables.get('order[0][dir]') # Descending or Ascending
        order_col = 'columns[' + str(order_idx) + '][data]'
        order_col_name = datatables.get(order_col)

        if 'no' in order_col_name:
            order_col_name = def_col

        if (order_dir == "desc"):
            order_col_name =  str('-' + order_col_name)

        model = models.BackendUnitsModel.objects     
        model = model.exclude(Q(name=None))

        id_def_data = list(model.order_by(def_col).values_list('id'))
        id_def_data = [list((idx+1, ) + id_def_data[idx]) for idx in range(len(id_def_data))]
   
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
        length = int(datatables.get('length')) if int(datatables.get('length')) > 0 else len(model)
        page_number = int(start / length + 1)
        paginator = Paginator(model, length)

        try:
            object_list = paginator.page(page_number).object_list
        except PageNotAnInteger:
            object_list = paginator.page(1).object_list
        except EmptyPage:
            object_list = paginator.page(1).object_list

        data = []

        for obj in object_list:

            data.append(
            {
                'checkbox': f'<div class="form-check"><input type="checkbox" class="form-check-input dt-checkboxes" name="select" onchange="pushValue(this);" id="check{obj.id}" value="{obj.id}"><label class="form-check-label" for="check{obj.id}">&nbsp;</label></div>',
                'no': [x for x in id_def_data if obj.id == x[1]][0][0],
                'name': obj.name,
                'desc': obj.desc,
                'actions': f'<a href="javascript:void(0);" onclick="updateUnit({obj.id})" class="action-icon"> <i class="mdi mdi-square-edit-outline"></i></a> <a href="javascript:void(0);" onclick="deleteUnit({obj.id})" class="action-icon"> <i class="mdi mdi-delete"></i></a>'
            })

        return {    
            'draw': draw,
            'recordsTotal': records_total,
            'recordsFiltered': records_filtered,
            'data': data,
        }

class BackendUnitsClassView(LoginRequiredMixin, View):

    def get(self, request):
        context = {
            'title' : 'Backend | Satuan Data',
            'data'  : models.BackendUnitsModel.objects.values(),
            'form'  : forms.BackendUnitForm()
        }

        return render(request, 'backend/table_statistics/units/units.html', context)


    def post(self, request):

        is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'
        if is_ajax:
            if request.method == 'POST':

                if request.POST.get('id'):
                    data = get_object_or_404(models.BackendUnitsModel, pk=request.POST.get('id'))
                    form = forms.BackendUnitForm(request.POST, instance=data)
                    msg = f'The Satuan Data Statistik “NAME” was changed successfully.'
                else:
                    form = forms.BackendUnitForm(request.POST)
                    msg = 'The Satuan Data Statistik “NAME” was added successfully.'

                if form.is_valid():
                    old_dt = form.cleaned_data.get('name')
                    form.save()
                    return JsonResponse({"status": 'success', 'message': msg.replace("NAME", old_dt)}, status=200)
                else:
                    return JsonResponse({"status": 'failed', "error": form.errors}, status=400)

        return JsonResponse({'status': 'Invalid request'}, status=400)

class BackendUnitDeleteClassView(LoginRequiredMixin, View):
    # Cleaned
    def post(self, request):
        is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'

        if is_ajax:
            if request.method == 'POST':
                try:
                    data = get_object_or_404(models.BackendUnitsModel, pk=request.POST.get('id'))
                    old_dt = data.name 
                    data.delete()
                    return JsonResponse({'status' : 'success', 'message': f'The Satuan Data Statistik "{old_dt}" was deleted successfully.'})
                except:
                    return JsonResponse({'status': 'failed', 'message': 'Data not available'})
                
        return JsonResponse({'status': 'Invalid request'}, status=400)
    

class BackendUnitMultipleDeleteClassView(LoginRequiredMixin, View):

    def post(self, request):
        is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'

        if is_ajax:
            if request.method == 'POST':

                try:
                
                    data = request.POST.getlist('valsId[]')
                    for dt in data:
                        model = get_object_or_404(models.BackendUnitsModel, pk=dt)
                        model.delete()   
                    return JsonResponse({'status': 'success', 'message': f'Successfully deleted {len(data)} units of data.'})
                except:
                    return JsonResponse({'status': 'failed', 'message': 'Something wrong'})

        return JsonResponse({'status': 'Invalid request'}, status=400)

class BackendUnitDetailClassView(LoginRequiredMixin, View):

    def post(self, request):
        is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'

        if is_ajax:
            if request.method == 'POST':
                
                id = request.POST.get('id')
                data = models.BackendUnitsModel.objects.filter(pk=id)

                if data.exists():
                    return JsonResponse({'status' : 'success', 'instance': list(data.values())[0]}, status=200)
                else:
                    return JsonResponse({'status': 'failed', 'message': 'Data tidak tersedia'}, status=200)
                
        return JsonResponse({'status': 'Invalid request'}, status=400) 

class BackendUnitsExportClassView(LoginRequiredMixin, View):

    def get(self, request):
    
        resource = resources.BackendUnitsResource()
        dataset = resource.export()

        response = HttpResponse(dataset.xls, content_type='application/vnd.ms-excel')
        response['Content-Disposition'] = 'attachment; filename="Satuan Data.xls"'
        return response 
    
# <========================================== END BACKEND UNITS ===============================================>



# <========================================== START BACKEND PERIODS ===============================================>
    
class BackendPeriodsItemsClassView(LoginRequiredMixin, View):

    def get(self, request):
        context = {
            'title' : 'Backend | Satuan Data',
            'form' : forms.BackendPeriodForm()
        }
        instance = models.BackendPeriodsModel.objects.get(pk=1)
        a = models.BackendPeriodNameItemsModel.objects.filter(pk=1,period_id=instance ).first()
        print(a)

        return render(request, 'backend/table_statistics/periods.html', context)

    def post(self, request):

        is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'

        if is_ajax:
            if request.method == 'POST':

                if len(request.POST.getlist('items[]')) == 0:
                    return JsonResponse({"status": 'failed', "error": 'Data items cannot be empty'}, status=400)
                
                if request.POST.get('id'):
                    if len(request.POST.getlist('items[]')) == 0:
                        return JsonResponse({"status": 'failed', "error": 'The data item cannot be empty if you want to update the data'}, status=400)
            
                    data = get_object_or_404(models.BackendPeriodsModel, pk=request.POST.get('id'))
                    form = forms.BackendPeriodForm(request.POST, instance=data)
                    msg = f'The period data statistic “NAME” was changed successfully.'
                else:
                    form = forms.BackendPeriodForm(request.POST)
                    msg = 'The period data statistic “NAME” was added successfully.'

                if form.is_valid():

                    old_dt = form.cleaned_data.get('name')
                    instance = form.save()
                    
                    if request.POST.get('id'):
                        
                        for id, item in zip(request.POST.getlist('ids[]'), request.POST.getlist('items[]')):

                            item_data = models.BackendPeriodNameItemsModel.objects.filter(pk=id,period_id=instance).first()
                            item_data.item_period = item
                            item_data.save()

                        return JsonResponse({"status": 'success', 'message': msg.replace("NAME", old_dt)}, status=200)
                    else:
                        for item in request.POST.getlist('items[]'):
                            models.BackendPeriodNameItemsModel(period_id = instance, item_period = item).save()

                        return JsonResponse({"status": 'success', 'message': msg.replace("NAME", old_dt)}, status=200)
                else:
                    return JsonResponse({"status": 'failed', "error": form.errors}, status=400)

        return JsonResponse({'status': 'Invalid request'}, status=400)

class BackendPeriodsJsonClassView(LoginRequiredMixin, View):

    def post(self, request):
        print('Hello world')
        data = self._datatables(request)
        return HttpResponse(json.dumps(data, cls=DjangoJSONEncoder), content_type='application/json')
		
    def _datatables(self, request):

        # Define default column for ordering first request
        def_col = 'name' 

        datatables = request.POST

        # Get Draw
        draw = int(datatables.get('draw'))
        start = int(datatables.get('start'))
        search = datatables.get('search[value]')

        order_idx = int(datatables.get('order[0][column]')) # Default 1st index for
        order_dir = datatables.get('order[0][dir]') # Descending or Ascending
        order_col = 'columns[' + str(order_idx) + '][data]'
        order_col_name = datatables.get(order_col)

        if 'no' in order_col_name:
            order_col_name = def_col

        if (order_dir == "desc"):
            order_col_name =  str('-' + order_col_name)

        model = models.BackendPeriodsModel.objects.prefetch_related('period_item')
        model = model.exclude(Q(name=None) | Q(period_item__item_period=None))

        id_def_data = list(model.order_by(def_col).values_list('id'))
        id_def_data = [list((idx+1, ) + id_def_data[idx]) for idx in range(len(id_def_data))]
        
        records_total = model.count()
        records_filtered = records_total
        
        
        if search:
            
            model = models.BackendPeriodsModel.objects.prefetch_related('period_item').filter(
                Q(name=search)|Q(period_item__item_period=search)
            ).exclude(Q(name=None) | Q(period_item__item_period=None))

            records_total = model.count()
            records_filtered = records_total
        

        model = model.order_by(order_col_name).values('id', 'name', 'period_item__item_period')

        data_periods = []

        for dt in model:

            idx = next((index for (index, d) in enumerate(data_periods) if d["id"] == dt['id']), None)

            if idx is not None:
                data_periods[idx]['period_item__item_period'].append(dt['period_item__item_period'])
            else:
                data_periods.append({
                    'id' : dt['id'],
                    'name' : dt['name'],
                    'period_item__item_period' : [dt['period_item__item_period'], ]
                })

        # Conf Paginator
        length = int(datatables.get('length')) if int(datatables.get('length')) > 0 else len(data_periods)
        page_number = int(start / length + 1)
        paginator = Paginator(data_periods, length)

        try:
            object_list = paginator.page(page_number).object_list
        except PageNotAnInteger:
            object_list = paginator.page(1).object_list
        except EmptyPage:
            object_list = paginator.page(1).object_list

        data = []

        for obj in object_list:

            data.append(
            {
                'checkbox': f'<div class="form-check"><input type="checkbox" class="form-check-input dt-checkboxes" name="select" onchange="pushValue(this);" id="check{obj["id"]}" value="{obj["id"]}"><label class="form-check-label" for="check{obj["id"]}">&nbsp;</label></div>',
                'no': [x for x in id_def_data if obj['id'] == x[1]][0][0],
                'name': obj['name'],
                'period_item__item_period': "; ".join(obj['period_item__item_period']),
                'actions': f'<a href="javascript:void(0);" onclick="updatePeriod({obj["id"]})" class="action-icon"> <i class="mdi mdi-square-edit-outline"></i></a> <a href="javascript:void(0);" onclick="deletePeriod({obj["id"]})" class="action-icon"> <i class="mdi mdi-delete"></i></a>'
            })

        return {    
            'draw': draw,
            'recordsTotal': records_total,
            'recordsFiltered': records_filtered,
            'data': data,
        }


class BackendPeriodsdDeleteClassView(LoginRequiredMixin, View):

    def post(self, request):
        is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'

        if is_ajax:
            if request.method == 'POST':
                print('Masukk')
                try:
                    data = get_object_or_404(models.BackendPeriodsModel, pk=request.POST.get('id'))
                    old_dt = data.name 
                    data.delete()
                    return JsonResponse({'status' : 'success', 'message': f'The periods data statistics "{old_dt}" was deleted successfully.'})
                except:
                    return JsonResponse({'status': 'failed', 'message': 'Data not available'})
                
        return JsonResponse({'status': 'Invalid request'}, status=400)


class BackendPeriodDetailClassView(LoginRequiredMixin, View):

    def post(self, request):
        is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'

        if is_ajax:
            if request.method == 'POST':
                
                id = request.POST.get('id')
                data = models.BackendPeriodsModel.objects.prefetch_related('period_item').filter(pk=id).order_by('period_item__id').values('id', 'name', 'period_item__item_period', 'period_item__id')

                data_period = {
                        'id' : None,
                        'name' : None,
                        'items' : []
                }   
                for dt in data:
                    data_period['id'] = dt['id']
                    data_period['name'] = dt['name']
                    data_period['items'].append(
                        {
                            'id' : dt['period_item__id'],
                            'item' : dt['period_item__item_period']
                        })

                if data.exists():
                    return JsonResponse({'status' : 'success', 'instance': data_period}, status=200)
                else:
                    return JsonResponse({'status': 'failed', 'message': 'Data tidak tersedia'}, status=200)
                
        return JsonResponse({'status': 'Invalid request'}, status=400)

# <========================================== END BACKEND PERIODS ===============================================>
    
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