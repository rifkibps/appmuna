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

import datetime
from operator import itemgetter
from datetime import datetime as datetime_

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

        return render(request, 'backend/table_statistics/periods.html', context)

    def post(self, request):

        is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'

        if is_ajax:
            if request.method == 'POST':
                
                if len(request.POST.getlist('items[]')) == 0:
                    return JsonResponse({"status": 'failed', "error": 'Data items cannot be empty'}, status=400)
                
                if request.POST.get('id'):
                    if len(request.POST.getlist('ids[]')) == 0:
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
                        
                        collect_ids = list(models.BackendPeriodsModel.objects.prefetch_related('period_item').filter(id=instance.id).values_list('period_item__id', flat=True))
                        
                        ids = request.POST.getlist('ids[]')
                        ids_for_del = [x for x in collect_ids if str(x) not in ids]

                        for id, item in zip(request.POST.getlist('ids[]'), request.POST.getlist('items[]')):
                            
                            if id == '':
                                models.BackendPeriodNameItemsModel(period_id = instance, item_period = item).save()
                            else:
                                item_data = models.BackendPeriodNameItemsModel.objects.filter(pk=id, period_id=instance).first()
                                item_data.item_period = item
                                item_data.save()

                        for id_ in ids_for_del:
                            models.BackendPeriodNameItemsModel.objects.filter(pk=id_).delete()

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
                Q(name__icontains=search)|Q(period_item__item_period__icontains=search)
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


            list_item = '<ol>'
            for item in obj['period_item__item_period']:
                list_item += f'<li>{item}</li>'
            list_item += '<ol>'

            data.append(
            {
                'checkbox': f'<div class="form-check"><input type="checkbox" class="form-check-input dt-checkboxes" name="select" onchange="pushValue(this);" id="check{obj["id"]}" value="{obj["id"]}"><label class="form-check-label" for="check{obj["id"]}">&nbsp;</label></div>',
                'no': [x for x in id_def_data if obj['id'] == x[1]][0][0],
                'name': obj['name'],
                'period_item__item_period': list_item,
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

                period_data = {
                        'id' : None,
                        'name' : None,
                        'items' : []
                }   
                for dt in data:
                    period_data['id'] = dt['id']
                    period_data['name'] = dt['name']
                    period_data['items'].append(
                        {
                            'id' : dt['period_item__id'],
                            'item' : dt['period_item__item_period']
                        })

                if data.exists():
                    return JsonResponse({'status' : 'success', 'instance': period_data}, status=200)
                else:
                    return JsonResponse({'status': 'failed', 'message': 'Data tidak tersedia'}, status=200)
                
        return JsonResponse({'status': 'Invalid request'}, status=400)

class BackendPeriodsMultipleDeleteClassView(LoginRequiredMixin, View):

    def post(self, request):
        is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'

        if is_ajax:
            if request.method == 'POST':

                try:
                    data = request.POST.getlist('valsId[]')
                    for dt in data:
                        model = get_object_or_404(models.BackendPeriodsModel, pk=dt)
                        model.delete()   
                    return JsonResponse({'status': 'success', 'message': f'Successfully deleted {len(data)} periods of data.'})
                except:
                    return JsonResponse({'status': 'failed', 'message': 'Something wrong'})

        return JsonResponse({'status': 'Invalid request'}, status=400)
    
class BackendPeriodsExportClassView(LoginRequiredMixin, View):

    def get(self, request):
    
        resource = resources.BackendPeriodsResource()
        dataset = resource.export()

        response = HttpResponse(dataset.xls, content_type='application/vnd.ms-excel')
        response['Content-Disposition'] = 'attachment; filename="Periode Data.xls"'
        return response 
    

# <========================================== END BACKEND PERIODS ===============================================>
    

    
# <========================================== START BACKEND ROWS ===============================================>

class BackendRowsItemsClassView(View):
    def get(self, request):
        context = {
            'title' : 'Backend | Kelompok Baris',
            'form' : forms.BackendRowForm()
        }
        return render(request, 'backend/table_statistics/rows.html', context)
    
    def post(self, request):

        is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'

        if is_ajax:
            if request.method == 'POST':
                if len(request.POST.getlist('item_rows[]')) == 0 or len(request.POST.getlist('order_nums[]')) == 0:
                    return JsonResponse({"status": 'failed', "error": 'Data items cannot be empty'}, status=400)
                
                if request.POST.get('id'):
                    if len(request.POST.getlist('ids[]')) == 0:
                        return JsonResponse({"status": 'failed', "error": 'The data item cannot be empty if you want to update the data'}, status=400)
                    
                    data = get_object_or_404(models.BackendRowsModel, pk=request.POST.get('id'))
                    form = forms.BackendRowForm(request.POST, instance=data)
                    msg = f'The row data statistic “NAME” was changed successfully.'
                else:
                    form = forms.BackendRowForm(request.POST)
                    msg = 'The row data statistic “NAME” was added successfully.'


                if form.is_valid():

                    old_dt = form.cleaned_data.get('name')
                    instance = form.save()
                    
                    if request.POST.get('id'):
                        
                        collect_ids = list(models.BackendRowsModel.objects.prefetch_related('row_items').filter(id=instance.id).values_list('row_items__id', flat=True))
                        
                        ids = request.POST.getlist('ids[]')
                        ids_for_del = [x for x in collect_ids if str(x) not in ids]

                        for id, num, item in zip(request.POST.getlist('ids[]'), request.POST.getlist('order_nums[]'), request.POST.getlist('item_rows[]')):
                            
                            if id == '':
                                models.BackendRowsItemsModel(row_id = instance, order_num = num, item_row = item).save()
                            else:
                                item_data = models.BackendRowsItemsModel.objects.filter(pk=id, row_id=instance).first()
                                item_data.order_num = num
                                item_data.item_row = item
                                item_data.save()

                        for id_ in ids_for_del:
                            models.BackendRowsItemsModel.objects.filter(pk=id_).delete()

                        return JsonResponse({"status": 'success', 'message': msg.replace("NAME", old_dt)}, status=200)
                    else:

                        for num, item in zip(request.POST.getlist('order_nums[]'), request.POST.getlist('item_rows[]')):
                            models.BackendRowsItemsModel(row_id = instance, order_num = num, item_row = item).save()

                        return JsonResponse({"status": 'success', 'message': msg.replace("NAME", old_dt)}, status=200)
                else:
                    return JsonResponse({"status": 'failed', "error": form.errors}, status=400)

        return JsonResponse({'status': 'Invalid request'}, status=400)
        
class BackendRowsJsonClassView(LoginRequiredMixin, View):

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

        model = models.BackendRowsModel.objects.prefetch_related('row_items')
        model = model.exclude(Q(name=None) | Q(row_items__order_num=None) | Q(row_items__item_row = None))

        id_def_data = list(model.order_by(def_col).values_list('id'))
        id_def_data = [list((idx+1, ) + id_def_data[idx]) for idx in range(len(id_def_data))]
        
        records_total = model.count()
        records_filtered = records_total
        
        
        if search:
            
            model = models.BackendRowsModel.objects.prefetch_related('row_items').filter(
                Q(name__icontains=search)|Q(row_items__item_row__icontains=search)
            ).exclude(Q(name=None) | Q(row_items__order_num=None) | Q(row_items__item_row = None))

            records_total = model.count()
            records_filtered = records_total
        

        model = model.order_by(order_col_name, 'row_items__order_num').values('id', 'name', 'row_items__order_num', 'row_items__item_row')

        data_periods = []

        for dt in model:

            idx = next((index for (index, d) in enumerate(data_periods) if d["id"] == dt['id']), None)

            if idx is not None:
                data_periods[idx]['row_items__item_row'].append([dt['row_items__order_num'], dt['row_items__item_row']])
            else:
                data_periods.append({
                    'id' : dt['id'],
                    'name' : dt['name'],
                    'row_items__item_row' : [
                        [dt['row_items__order_num'], dt['row_items__item_row']]
                    ]
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

            list_item = '<ul style="list-style-type:none">'
            for item in obj['row_items__item_row']:
                list_item += f'<li>{item[0]}. {item[1]}</li>'
            list_item += '<ul>'

            data.append(
            {
                'checkbox': f'<div class="form-check"><input type="checkbox" class="form-check-input dt-checkboxes" name="select" onchange="pushValue(this);" id="check{obj["id"]}" value="{obj["id"]}"><label class="form-check-label" for="check{obj["id"]}">&nbsp;</label></div>',
                'no': [x for x in id_def_data if obj['id'] == x[1]][0][0],
                'name': obj['name'],
                'row_items__item_row': list_item,
                'actions': f'<a href="javascript:void(0);" onclick="updateRow({obj["id"]})" class="action-icon"> <i class="mdi mdi-square-edit-outline"></i></a> <a href="javascript:void(0);" onclick="deleteRow({obj["id"]})" class="action-icon"> <i class="mdi mdi-delete"></i></a>'
            })

        return {    
            'draw': draw,
            'recordsTotal': records_total,
            'recordsFiltered': records_filtered,
            'data': data,
        }

class BackendRowDetailClassView(LoginRequiredMixin, View):

    def post(self, request):
        is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'

        if is_ajax:
            if request.method == 'POST':
                
                id = request.POST.get('id')
                data = models.BackendRowsModel.objects.prefetch_related('row_items').filter(pk=id).order_by('row_items__order_num').values('id', 'name', 'row_items__id', 'row_items__order_num', 'row_items__item_row', )

                row_data = {
                        'id' : None,
                        'name' : None,
                        'items' : []
                }   
                for dt in data:
                    row_data['id'] = dt['id']
                    row_data['name'] = dt['name']
                    row_data['items'].append(
                        {
                            'id' : dt['row_items__id'],
                            'order_num' : dt['row_items__order_num'],
                            'item_row' : dt['row_items__item_row']
                    })

                if data.exists():
                    return JsonResponse({'status' : 'success', 'instance': row_data}, status=200)
                else:
                    return JsonResponse({'status': 'failed', 'message': 'Data tidak tersedia'}, status=200)
                
        return JsonResponse({'status': 'Invalid request'}, status=400)

class BackendRowDeleteClassView(LoginRequiredMixin, View):

    def post(self, request):
        is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'

        if is_ajax:
            if request.method == 'POST':
                try:
                    data = get_object_or_404(models.BackendRowsModel, pk=request.POST.get('id'))
                    old_dt = data.name 
                    data.delete()
                    return JsonResponse({'status' : 'success', 'message': f'The rows data statistics "{old_dt}" was deleted successfully.'})
                except:
                    return JsonResponse({'status': 'failed', 'message': 'Data not available'})
                
        return JsonResponse({'status': 'Invalid request'}, status=400)

class BackendRowsMultipleDeleteClassView(LoginRequiredMixin, View):

    def post(self, request):
        is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'

        if is_ajax:
            if request.method == 'POST':

                try:
                    data = request.POST.getlist('valsId[]')
                    for dt in data:
                        model = get_object_or_404(models.BackendRowsModel, pk=dt)
                        model.delete()   
                    return JsonResponse({'status': 'success', 'message': f'Successfully deleted {len(data)} rows of data.'})
                except:
                    return JsonResponse({'status': 'failed', 'message': 'Something wrong'})

        return JsonResponse({'status': 'Invalid request'}, status=400)
    
class BackendRowsExportClassView(LoginRequiredMixin, View):

    def get(self, request):
    
        resource = resources.BackendRowsResource()
        dataset = resource.export()

        response = HttpResponse(dataset.xls, content_type='application/vnd.ms-excel')
        response['Content-Disposition'] = 'attachment; filename="Data Judul Baris.xls"'
        return response 


# <========================================== END BACKEND ROWS ===============================================>




# <========================================== START BACKEND CHARACTERISTICS ===============================================>

class BackendCharsClassView(View):
    def get(self, request):
        context = {
            'title' : 'Backend | Karakteristik Data',
            'form' : forms.BackendCharForm()
        }
        return render(request, 'backend/table_statistics/characteristics.html', context)

    def post(self, request):

        is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'

        if is_ajax:
            if request.method == 'POST':
                if len(request.POST.getlist('item_chars[]')) == 0:
                    return JsonResponse({"status": 'failed', "error": 'Data items cannot be empty'}, status=400)
                
                if request.POST.get('id'):
                    if len(request.POST.getlist('ids[]')) == 0:
                        return JsonResponse({"status": 'failed', "error": 'The data item cannot be empty if you want to update the data'}, status=400)
                    
                    data = get_object_or_404(models.BackendCharacteristicsModel, pk=request.POST.get('id'))
                    form = forms.BackendCharForm(request.POST, instance=data)
                    msg = f'The row data statistic “NAME” was changed successfully.'
                else:
                    form = forms.BackendCharForm(request.POST)
                    msg = 'The row data statistic “NAME” was added successfully.'


                if form.is_valid():

                    old_dt = form.cleaned_data.get('name')
                    instance = form.save()
                    
                    if request.POST.get('id'):
                        
                        collect_ids = list(models.BackendCharacteristicsModel.objects.prefetch_related('characteristic_items').filter(id=instance.id).values_list('characteristic_items__id', flat=True))
                        
                        ids = request.POST.getlist('ids[]')
                        ids_for_del = [x for x in collect_ids if str(x) not in ids]

                        for id, item in zip(request.POST.getlist('ids[]'), request.POST.getlist('item_chars[]')):
                            
                            if id == '':
                                models.BackendCharacteristicItemsModel(char_id = instance, item_char = item).save()
                            else:
                                item_data = models.BackendCharacteristicItemsModel.objects.filter(pk=id, char_id=instance).first()
                                item_data.item_char = item
                                item_data.save()

                        for id_ in ids_for_del:
                            models.BackendCharacteristicItemsModel.objects.filter(pk=id_).delete()

                        return JsonResponse({"status": 'success', 'message': msg.replace("NAME", old_dt)}, status=200)
                    
                    else:
                        
                        for item in request.POST.getlist('item_chars[]'):
                            models.BackendCharacteristicItemsModel(char_id = instance, item_char = item).save()

                        return JsonResponse({"status": 'success', 'message': msg.replace("NAME", old_dt)}, status=200)
                else:
                    return JsonResponse({"status": 'failed', "error": form.errors}, status=400)

        return JsonResponse({'status': 'Invalid request'}, status=400)

class BackendCharsJsonClassView(LoginRequiredMixin, View):

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

        model = models.BackendCharacteristicsModel.objects.prefetch_related('characteristic_items')
        model = model.exclude(Q(name=None) | Q(characteristic_items__item_char = None))

        id_def_data = list(model.order_by(def_col).values_list('id'))
        id_def_data = [list((idx+1, ) + id_def_data[idx]) for idx in range(len(id_def_data))]
        
        records_total = model.count()
        records_filtered = records_total
        
        
        if search:
            model = models.BackendCharacteristicsModel.objects.prefetch_related('characteristic_items').filter(
                Q(name__icontains=search)|Q(characteristic_items__item_char__icontains=search)
            ).exclude(Q(name=None) | Q(characteristic_items__item_char = None))

            records_total = model.count()
            print(search)
            print(records_total)
            records_filtered = records_total
        

        model = model.order_by(order_col_name).values('id', 'name', 'characteristic_items__item_char')

        data_periods = []

        for dt in model:

            idx = next((index for (index, d) in enumerate(data_periods) if d["id"] == dt['id']), None)

            if idx is not None:
                data_periods[idx]['characteristic_items__item_char'].append(dt['characteristic_items__item_char'])
            else:
                data_periods.append({
                    'id' : dt['id'],
                    'name' : dt['name'],
                    'characteristic_items__item_char' : [
                        dt['characteristic_items__item_char']
                    ]
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

            list_item = '<ol>'
            for item in obj['characteristic_items__item_char']:
                list_item += f'<li>{item}</li>'
            list_item += '<ol>'

            data.append(
            {
                'checkbox': f'<div class="form-check"><input type="checkbox" class="form-check-input dt-checkboxes" name="select" onchange="pushValue(this);" id="check{obj["id"]}" value="{obj["id"]}"><label class="form-check-label" for="check{obj["id"]}">&nbsp;</label></div>',
                'no': [x for x in id_def_data if obj['id'] == x[1]][0][0],
                'name': obj['name'],
                'characteristic_items__item_char': list_item,
                'actions': f'<a href="javascript:void(0);" onclick="updateChar({obj["id"]})" class="action-icon"> <i class="mdi mdi-square-edit-outline"></i></a> <a href="javascript:void(0);" onclick="deleteChar({obj["id"]})" class="action-icon"> <i class="mdi mdi-delete"></i></a>'
            })

        return {    
            'draw': draw,
            'recordsTotal': records_total,
            'recordsFiltered': records_filtered,
            'data': data,
        }

class BackendCharDeleteClassView(LoginRequiredMixin, View):

    def post(self, request):
        is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'

        if is_ajax:
            if request.method == 'POST':
                try:
                    data = get_object_or_404(models.BackendCharacteristicsModel, pk=request.POST.get('id'))
                    old_dt = data.name 
                    data.delete()
                    return JsonResponse({'status' : 'success', 'message': f'The rows data statistics "{old_dt}" was deleted successfully.'})
                except:
                    return JsonResponse({'status': 'failed', 'message': 'Data not available'})
                
        return JsonResponse({'status': 'Invalid request'}, status=400)

class BackendCharsMultipleDeleteClassView(LoginRequiredMixin, View):
    
    def post(self, request):
        is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'

        if is_ajax:
            if request.method == 'POST':

                try:
                    data = request.POST.getlist('valsId[]')
                    for dt in data:
                        model = get_object_or_404(models.BackendCharacteristicsModel, pk=dt)
                        model.delete()   
                    return JsonResponse({'status': 'success', 'message': f'Successfully deleted {len(data)} rows of data.'})
                except:
                    return JsonResponse({'status': 'failed', 'message': 'Something wrong'})

        return JsonResponse({'status': 'Invalid request'}, status=400)
    
class BackendCharDetailClassView(LoginRequiredMixin, View):

    def post(self, request):
        is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'

        if is_ajax:
            if request.method == 'POST':
                
                id = request.POST.get('id')
                data = models.BackendCharacteristicsModel.objects.prefetch_related('characteristic_items').filter(pk=id).values('id', 'name', 'characteristic_items__id', 'characteristic_items__item_char')

                row_data = {
                        'id' : None,
                        'name' : None,
                        'items' : []
                }

                for dt in data:
                    row_data['id'] = dt['id']
                    row_data['name'] = dt['name']
                    row_data['items'].append(
                        {
                            'id' : dt['characteristic_items__id'],
                            'item_char' : dt['characteristic_items__item_char']
                    })

                if data.exists():
                    return JsonResponse({'status' : 'success', 'instance': row_data}, status=200)
                else:
                    return JsonResponse({'status': 'failed', 'message': 'Data tidak tersedia'}, status=200)
                
        return JsonResponse({'status': 'Invalid request'}, status=400)

# <========================================== End BACKEND CHARACTERISTICS ===============================================>
    


# <========================================== Start Backend Subjects ===============================================>


class BackendSubjectsClassView(View):

    def get(self, request):
        context = {
            'title' : 'Backend | Subject Statistik',
            'form'  : forms.BackendSubjectForm()
        }

        return render(request, 'backend/table_statistics/subjects.html', context)

    def post(self, request):

        is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'
        if is_ajax:
            if request.method == 'POST':

                if request.POST.get('id'):
                    data = get_object_or_404(models.BackendSubjectsModel, pk=request.POST.get('id'))
                    form = forms.BackendSubjectForm(request.POST, instance=data)
                    msg = f'The subject data statistik “NAME” was changed successfully.'
                else:
                    form = forms.BackendSubjectForm(request.POST)
                    msg = 'The subject data statistik “NAME” was added successfully.'

                if form.is_valid():
                    old_dt = form.cleaned_data.get('name')
                    form.save()
                    return JsonResponse({"status": 'success', 'message': msg.replace("NAME", old_dt)}, status=200)
                else:
                    return JsonResponse({"status": 'failed', "error": form.errors}, status=400)

        return JsonResponse({'status': 'Invalid request'}, status=400)

class BackendSubjectsJsonClassView(LoginRequiredMixin, View):

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

        model = models.BackendSubjectsModel.objects     
        model = model.exclude(Q(name=None) | Q(subject_group=None) | Q(show_state=None))

        id_def_data = list(model.order_by(def_col).values_list('id'))
        id_def_data = [list((idx+1, ) + id_def_data[idx]) for idx in range(len(id_def_data))]
   
        records_total = model.count()
        records_filtered = records_total
        
        if search:
            model = models.BackendSubjectsModel.objects.filter(
                Q(name__icontains=search)
            ).exclude(Q(name=None) | Q(subject_group=None) | Q(show_state=None))

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

            checked = 'checked' if obj.show_state == '1' else ''
            data.append(
            {
                'checkbox': f'<div class="form-check"><input type="checkbox" class="form-check-input dt-checkboxes" name="select" onchange="pushValue(this);" id="check{obj.id}" value="{obj.id}"><label class="form-check-label" for="check{obj.id}">&nbsp;</label></div>',
                'no': [x for x in id_def_data if obj.id == x[1]][0][0],
                'name': obj.name,
                'subject_group': obj.get_subject_group_display(),
                'show_state': f'<div class="form-check form-switch"><input type="checkbox" class="form-check-input" onchange="switchState(this)" id="customSwitch{obj.id}" data-id="{obj.id}" value="1" {checked}></div>',
                'actions': f'<a href="javascript:void(0);" onclick="updateSubject({obj.id})" class="action-icon"> <i class="mdi mdi-square-edit-outline"></i></a> <a href="javascript:void(0);" onclick="deleteSubject({obj.id})" class="action-icon"> <i class="mdi mdi-delete"></i></a>'
            })

        return {    
            'draw': draw,
            'recordsTotal': records_total,
            'recordsFiltered': records_filtered,
            'data': data,
        }

class BackendSubjectDeleteClassView(LoginRequiredMixin, View):

    def post(self, request):
        is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'

        if is_ajax:
            if request.method == 'POST':
                try:
                    data = get_object_or_404(models.BackendSubjectsModel, pk=request.POST.get('id'))
                    old_dt = data.name 
                    data.delete()
                    return JsonResponse({'status' : 'success', 'message': f'The subject data statistics "{old_dt}" was deleted successfully.'})
                except:
                    return JsonResponse({'status': 'failed', 'message': 'Data not available'})
                
        return JsonResponse({'status': 'Invalid request'}, status=400)

class BackendSubjectsMultipleDeleteClassView(LoginRequiredMixin, View):
    
    def post(self, request):
        is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'

        if is_ajax:
            if request.method == 'POST':

                try:
                    data = request.POST.getlist('valsId[]')
                    for dt in data:
                        model = get_object_or_404(models.BackendSubjectsModel, pk=dt)
                        model.delete()   
                    return JsonResponse({'status': 'success', 'message': f'Successfully deleted {len(data)} rows of data.'})
                except:
                    return JsonResponse({'status': 'failed', 'message': 'Something wrong'})

        return JsonResponse({'status': 'Invalid request'}, status=400)
    
class BackendSubjectSwitchStateClassView(LoginRequiredMixin, View):
    
    def post(self, request):
        is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'

        if is_ajax:
            if request.method == 'POST':
                try:
                    data = get_object_or_404(models.BackendSubjectsModel, pk=request.POST.get('id'))
                    old_dt = data.name
                    current_state = '2' if data.show_state == '1' else '1'
                    data.show_state = current_state
                    data.save()
                    return JsonResponse({'status' : 'success', 'message': f'The subject data statistics "{old_dt}" was updated successfully.'})
                except:
                    return JsonResponse({'status': 'failed', 'message': 'Data not available'})
                
        return JsonResponse({'status': 'Invalid request'}, status=400)
    
class BackendSubjectDetailClassView(LoginRequiredMixin, View):

    def post(self, request):
        is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'

        if is_ajax:
            if request.method == 'POST':
                
                id = request.POST.get('id')
                data = models.BackendSubjectsModel.objects.filter(pk=id)

                if data.exists():
                    return JsonResponse({'status' : 'success', 'instance': list(data.values())[0]}, status=200)
                else:
                    return JsonResponse({'status': 'failed', 'message': 'Data tidak tersedia'}, status=200)
                
        return JsonResponse({'status': 'Invalid request'}, status=400) 

class BackendSubjectsExportClassView(LoginRequiredMixin, View):

    def get(self, request):
    
        resource = resources.BackendSubjectResource()
        dataset = resource.export()

        response = HttpResponse(dataset.xls, content_type='application/vnd.ms-excel')
        response['Content-Disposition'] = 'attachment; filename="Data Subject.xls"'
        return response 



# <========================================== end Backend Subjects ===============================================>
    

# <========================================== start Backend Content ===============================================>

class BackendIndicatorsClassView(View):
    
    def get(self, request):
        context = {
            'title' : 'Backend | Tabel Statistik',
            'form' : forms.BackendIndicatorForm
        }
        return render(request, 'backend/table_statistics/indicators.html', context)
    
    def post(self, request):

        is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'
        if is_ajax:
            if request.method == 'POST':

                if request.POST.get('id'):
                    data = get_object_or_404(models.BackendIndicatorsModel, pk=request.POST.get('id'))
                    form = forms.BackendIndicatorForm(request.POST, instance=data)
                    msg = f'The subject data statistik “NAME” was changed successfully.'
                else:
                    form = forms.BackendIndicatorForm(request.POST)
                    msg = 'The subject data statistik “NAME” was added successfully.'

                if form.is_valid():
                    old_dt = form.cleaned_data.get('name')
                    form.save()
                    return JsonResponse({"status": 'success', 'message': msg.replace("NAME", old_dt)}, status=200)
                else:
                    return JsonResponse({"status": 'failed', "error": form.errors}, status=400)

        return JsonResponse({'status': 'Invalid request'}, status=400)

class BackendIndicatorsJsonClassView(LoginRequiredMixin, View):

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

        
        model = models.BackendIndicatorsModel.objects   
        model = model.exclude(
            Q(subject_id=None) |
            Q(name=None) |
            Q(desc=None) |
            Q(footer_desc=None) |
            Q(row_group_id=None) |
            Q(time_period_id=None) |
            Q(unit_id=None) |
            Q(decimal_point=None) |
            Q(stat_category=None) |
            Q(show_state=None)
        )

        id_def_data = list(model.order_by(def_col).values_list('id'))
        id_def_data = [list((idx+1, ) + id_def_data[idx]) for idx in range(len(id_def_data))]
   
        records_total = model.count()
        records_filtered = records_total
        
        if search:
            model = models.BackendIndicatorsModel.objects.filter(
                Q(subject_id__name__icontains=search) |
                Q(name__icontains=search) |
                Q(stat_category__icontains=search) |
                Q(time_period_id__name__icontains=search)
            ).exclude(
            Q(subject_id=None) |
            Q(name=None) |
            Q(desc=None) |
            Q(footer_desc=None) |
            Q(row_group_id=None) |
            Q(time_period_id=None) |
            Q(unit_id=None) |
            Q(decimal_point=None) |
            Q(stat_category=None) |
            Q(show_state=None)
        )

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

            checked = 'checked' if obj.show_state == '1' else ''
            data.append(
            {
                'checkbox': f'<div class="form-check"><input type="checkbox" class="form-check-input dt-checkboxes" name="select" onchange="pushValue(this);" id="check{obj.id}" value="{obj.id}"><label class="form-check-label" for="check{obj.id}">&nbsp;</label></div>',
                'no': [x for x in id_def_data if obj.id == x[1]][0][0],
                'subject_id': obj.subject_id.name,
                'name': obj.name,
                'stat_category': obj.get_stat_category_display(),
                'time_period_id': obj.time_period_id.name,
                'show_state': f'<div class="form-check form-switch"><input type="checkbox" class="form-check-input" onchange="switchState(this)" id="customSwitch{obj.id}" data-id="{obj.id}" value="1" {checked}></div>',
                'actions': f'<a href="javascript:void(0);" onclick="updateIndicator({obj.id})" class="action-icon"> <i class="mdi mdi-square-edit-outline"></i></a> <a href="javascript:void(0);" onclick="deleteIndicator({obj.id})" class="action-icon"> <i class="mdi mdi-delete"></i></a>'
            })

        return {    
            'draw': draw,
            'recordsTotal': records_total,
            'recordsFiltered': records_filtered,
            'data': data,
        }

class BackendIndicatorSwitchStateClassView(LoginRequiredMixin, View):
    
    def post(self, request):
        is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'

        if is_ajax:
            if request.method == 'POST':
                try:
                    data = get_object_or_404(models.BackendIndicatorsModel, pk=request.POST.get('id'))
                    old_dt = data.name
                    current_state = '2' if data.show_state == '1' else '1'
                    data.show_state = current_state
                    data.save()
                    return JsonResponse({'status' : 'success', 'message': f'The indicator data statistics "{old_dt}" was updated successfully.'})
                except:
                    return JsonResponse({'status': 'failed', 'message': 'Data not available'})
                
        return JsonResponse({'status': 'Invalid request'}, status=400)
    
class BackendIndicatorDetailClassView(LoginRequiredMixin, View):

    def post(self, request):
        is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'

        if is_ajax:
            if request.method == 'POST':
                
                id = request.POST.get('id')
                data = models.BackendIndicatorsModel.objects.filter(pk=id)

                if data.exists():
                    return JsonResponse({'status' : 'success', 'instance': list(data.values())[0]}, status=200)
                else:
                    return JsonResponse({'status': 'failed', 'message': 'Data tidak tersedia'}, status=200)
                
        return JsonResponse({'status': 'Invalid request'}, status=400)
    
class BackendIndicatorDeleteClassView(LoginRequiredMixin, View):

    def post(self, request):
        is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'

        if is_ajax:
            if request.method == 'POST':
                try:
                    data = get_object_or_404(models.BackendIndicatorsModel, pk=request.POST.get('id'))
                    old_dt = data.name 
                    data.delete()
                    return JsonResponse({'status' : 'success', 'message': f'The indicators data statistics "{old_dt}" was deleted successfully.'})
                except:
                    return JsonResponse({'status': 'failed', 'message': 'Data not available'})
                
        return JsonResponse({'status': 'Invalid request'}, status=400)

class BackendIndicatorsMultipleDeleteClassView(LoginRequiredMixin, View):
    
    def post(self, request):
        is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'

        if is_ajax:
            if request.method == 'POST':

                try:
                    data = request.POST.getlist('valsId[]')
                    for dt in data:
                        model = get_object_or_404(models.BackendIndicatorsModel, pk=dt)
                        model.delete()   
                    return JsonResponse({'status': 'success', 'message': f'Successfully deleted {len(data)} rows of data.'})
                except:
                    return JsonResponse({'status': 'failed', 'message': 'Something wrong'})

        return JsonResponse({'status': 'Invalid request'}, status=400)

class BackendIndicatorsExportClassView(LoginRequiredMixin, View):

    def get(self, request):
    
        resource = resources.BackendIndicatorResource()
        dataset = resource.export()

        response = HttpResponse(dataset.xls, content_type='application/vnd.ms-excel')
        response['Content-Disposition'] = 'attachment; filename="Data Indikator.xls"'
        return response 


# <========================================== end Backend Content ===============================================>
    
class BackendContentClassView(View):
    
    def get(self, request):
        context = {
            'title' : 'Backend | Tabel Statistik',
        }
        return render(request, 'backend/table_statistics/content/manage.html', context)

class BackendContentJsonClassView(LoginRequiredMixin, View):

    def post(self, request):
        
        data = self._datatables(request)
        return HttpResponse(json.dumps(data, cls=DjangoJSONEncoder), content_type='application/json')
		
    def _datatables(self, request):

        # Define default column for ordering first request
        def_col = 'indicator_id__subject_id__name' 

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

        model = models.BackendContentIndicatorsModel.objects   
        model = model.exclude(
            Q(indicator_id=None) |
            Q(year=None) |
            Q(item_period=None) |
            Q(item_row=None) |
            Q(value=None)
        )

        id_def_data = list(model.order_by(def_col).values_list('id'))
        id_def_data = [list((idx+1, ) + id_def_data[idx]) for idx in range(len(id_def_data))]
   
        records_total = model.count()
        records_filtered = records_total
        
        if search:
            model = models.BackendContentIndicatorsModel.objects.filter(
                Q(indicator_id__subject_id__name__icontains=search) |
                Q(indicator_id__name__icontains=search) |
                Q(year__icontains=search)
            ).exclude(
            Q(indicator_id=None) |
            Q(year=None) |
            Q(item_period=None) |
            Q(item_row=None) |
            Q(value=None)
        )

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
                'indicator_id__subject_id__name': obj.indicator_id.subject_id.name,
                'indicator_id__name': obj.indicator_id.name,
                'indicator_id__stat_category': obj.indicator_id.get_stat_category_display(),
                'indicator_id__time_period_id__name': obj.indicator_id.time_period_id.name,
                'year': obj.year,
                'created_at' : obj.created_at.strftime('%d-%m-%Y'),
                'updated_at' : obj.updated_at.strftime('%d-%m-%Y'),
                'actions': f'<a href="javascript:void(0);" onclick="updateContent({obj.id})" class="action-icon"> <i class="mdi mdi-square-edit-outline"></i></a> <a href="javascript:void(0);" onclick="deleteContent({obj.id})" class="action-icon"> <i class="mdi mdi-delete"></i></a>'
            })

        return {    
            'draw': draw,
            'recordsTotal': records_total,
            'recordsFiltered': records_filtered,
            'data': data,
        }
    
class BackendContentDeleteClassView(LoginRequiredMixin, View):

    def post(self, request):
        is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'

        if is_ajax:
            if request.method == 'POST':
                try:
                    data = get_object_or_404(models.BackendContentIndicatorsModel, pk=request.POST.get('id'))
                    old_dt = data.indicator_id.name 
                    data.delete()
                    return JsonResponse({'status' : 'success', 'message': f'The table data statistics "{old_dt}" was deleted successfully.'})
                except:
                    return JsonResponse({'status': 'failed', 'message': 'Data not available'})
                
        return JsonResponse({'status': 'Invalid request'}, status=400)

class BackendContentMultipleDeleteClassView(LoginRequiredMixin, View):
    
    def post(self, request):
        is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'

        if is_ajax:
            if request.method == 'POST':
                try:
                    data = request.POST.getlist('valsId[]')
                    for dt in data:
                        model = get_object_or_404(models.BackendContentIndicatorsModel, pk=dt)
                        model.delete()   
                    return JsonResponse({'status': 'success', 'message': f'Successfully deleted {len(data)} rows of data.'})
                except:
                    return JsonResponse({'status': 'failed', 'message': 'Something wrong'})

        return JsonResponse({'status': 'Invalid request'}, status=400)

class BackendContentExportClassView(LoginRequiredMixin, View):

    def get(self, request):
    
        resource = resources.BackendContentResource()
        dataset = resource.export()

        response = HttpResponse(dataset.xls, content_type='application/vnd.ms-excel')
        response['Content-Disposition'] = 'attachment; filename="Data Konten Tabel.xls"'
        return response 

class BackendContentInputClassView(View):
    
    def get(self, request):

        context = {
            'title' :   'Backend | Tabel Statistik',
            'subjects' : models.BackendSubjectsModel.objects.values(),
        }

        years = datetime.datetime.today().year
        context['years'] = list(range(years+16, years - 25, -1))
        
        if request.GET.get('subject_id') and request.GET.get('indicator_id_select') and request.GET.get('year') and request.GET.get('periode_id'):




            context['d_form'] = 'submitted'
            subject_id = request.GET.get('subject_id')
            indicator_id = request.GET.get('indicator_id_select')
            year = request.GET.get('year')
            period_item_id = request.GET.get('periode_id')
            
            data_indicator = get_object_or_404(models.BackendIndicatorsModel, pk=indicator_id)
            
            data_contents = models.BackendContentIndicatorsModel.objects.filter(indicator_id=indicator_id, year=year, item_period = period_item_id).values()
            
            data_content_table = []
            for dt in data_contents:
                data_content_table.append({
                    dt["item_row"] : {dt["item_char"] : dt["value"]},
                })

            context['data_contents'] = data_content_table

            context['data_indicator'] = data_indicator
            context['created_at'] = data_indicator.created_at.strftime('%d %B %Y'),
            context['updated_at'] = data_indicator.updated_at.strftime('%d %B %Y'),

            data_rows = models.BackendRowsItemsModel.objects.filter(row_id = data_indicator.row_group_id).order_by('order_num')
            context['rows_groups'] = data_rows.values()

            context['subject_csa'] = data_indicator.subject_csa_id.name if data_indicator.subject_csa_id is not None else '-'
            context['col_groups'] = ['Tidak tersedia']
            context['col_group_name'] = ''
            context['range'] = range(1, 4)
            if data_indicator.col_group_id is not None:
                data_chars = models.BackendCharacteristicItemsModel.objects.filter(char_id = data_indicator.col_group_id).order_by('id')
                context['col_groups'] = data_chars.values()
                context['range'] = range(1, 3 + data_chars.count())
            
            context['col_group_name'] = data_indicator.subject_id.name
            context['row_group_name'] = data_rows.first().row_id.name

            context['current_year'] = int(year)
            context['subject_id'] = subject_id
            context['period'] = get_object_or_404(models.BackendPeriodNameItemsModel, pk=period_item_id)
            context['period_items'] = models.BackendPeriodNameItemsModel.objects.filter(period_id=data_indicator.time_period_id)
            context['indicators'] = models.BackendIndicatorsModel.objects.filter(subject_id=subject_id).values()

        return render(request, 'backend/table_statistics/content/input.html', context)


    def post(self, request):
        is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'

        if is_ajax:
            if request.method == 'POST':
                
                subject_id = request.POST.get('subject_id')
                indicator_id = request.POST.get('indicator_id')

                if subject_id:
                    data = models.BackendIndicatorsModel.objects.filter(subject_id=subject_id)

                    if data.exists():
                        opt = '<option value="" selected>Pilih Indikator</option>'
                        for dt in data:
                            opt += f'<option value="{dt.id}">{dt.name}</option>'

                        return JsonResponse({'status' : 'success', 'instance': opt}, status=200)
                    else:
                        opt = '<option selected>Data indikator belum tersedia</option>'
                        return JsonResponse({'status': 'failed', 'message': 'Data indikator belum tersedia', 'instance' : opt}, status=200)
                
                if indicator_id:
                    data = models.BackendIndicatorsModel.objects.filter(pk=indicator_id)
                    if data.exists():
                        items_period = models.BackendPeriodNameItemsModel.objects.filter(period_id=data.first().time_period_id)
                        
                        opt = '<option value="" selected>Pilih Turunan Tahun</option>'
                        for dt in items_period:
                            opt += f'<option value="{dt.id}">{dt.item_period}</option>'

                        return JsonResponse({'status' : 'success', 'instance': opt}, status=200)
                    else:
                        opt = '<option selected>Data indikator belum tersedia</option>'
                        return JsonResponse({'status': 'failed', 'message': 'Data indikator belum tersedia', 'instance' : opt}, status=200)
        return JsonResponse({'status': 'Invalid request'}, status=400)


class BackendContentInputFormClassView(LoginRequiredMixin, View):

    def post(self, request):
        is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'

        if is_ajax:
            if request.method == 'POST':
                
                subject_id = request.POST.get('subject_id')
                indicator_id = request.POST.get('indicator_id')

                if subject_id:
                    data = models.BackendIndicatorsModel.objects.filter(subject_id=subject_id)

                    if data.exists():
                        opt = '<option value="" selected>Pilih Indikator</option>'
                        for dt in data:
                            opt += f'<option value="{dt.id}">{dt.name}</option>'

                        return JsonResponse({'status' : 'success', 'instance': opt}, status=200)
                    else:
                        opt = '<option selected>Data indikator belum tersedia</option>'
                        return JsonResponse({'status': 'failed', 'message': 'Data indikator belum tersedia', 'instance' : opt}, status=200)
                
                if indicator_id:
                    data = models.BackendIndicatorsModel.objects.filter(pk=indicator_id)
                    if data.exists():
                        items_period = models.BackendPeriodNameItemsModel.objects.filter(period_id=data.first().time_period_id)
                        
                        opt = '<option value="" selected>Pilih Turunan Tahun</option>'
                        for dt in items_period:
                            opt += f'<option value="{dt.id}">{dt.item_period}</option>'

                        print(opt)
                        return JsonResponse({'status' : 'success', 'instance': opt}, status=200)
                    else:
                        opt = '<option selected>Data indikator belum tersedia</option>'
                        return JsonResponse({'status': 'failed', 'message': 'Data indikator belum tersedia', 'instance' : opt}, status=200)
        return JsonResponse({'status': 'Invalid request'}, status=400)
    

class BackendContentInputFormSubmitClassView(LoginRequiredMixin, View):
    
    def post(self, request):
        is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'

        if is_ajax:
            if request.method == 'POST':
                
                model = models.BackendContentIndicatorsModel

                data_request = request.POST
                indicator_id = data_request.get('indicator_id')
                year = data_request.get('year')
                item_period = data_request.get('item_period')

                indicator_data = get_object_or_404(models.BackendIndicatorsModel, pk=indicator_id)
                chars_item = models.BackendCharacteristicItemsModel.objects.filter(char_id = indicator_data.col_group_id).order_by('id')
                rows_item = models.BackendRowsItemsModel.objects.filter(row_id = indicator_data.row_group_id).order_by('id')

                objs_bulk_create = []
                for key, value in data_request.items():
                    if key in ['csrfmiddlewaretoken', 'indicator_id', 'year', 'item_period']:
                        continue
                    
                    row_item_id, col_item_id = key.split('-')
                    
                    objs_bulk_create.append(
                        model(
                            indicator_id = indicator_data,
                            year = year,
                            item_period = item_period,
                            item_char = col_item_id,
                            item_row = row_item_id,
                            value = data_request.get(key)
                        )
                    )

                if len(objs_bulk_create) > 0:
                    message = f'Data for the indicator <strong><i>"{indicator_data.name}"</i></strong> has been successfully updated on <strong>{datetime_.today().strftime('%d %B %Y')}</strong>.'
                    model.objects.bulk_create(objs_bulk_create)
                    return JsonResponse({'status': 'success', 'message' : message}, status=200)
                else:
                    return JsonResponse({'status': 'failed', 'message' : 'The indicator table content data is empty'}, status=200)
        return JsonResponse({'status': 'Invalid request'}, status=400)
    