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