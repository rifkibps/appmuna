from django.urls import reverse_lazy

from django.shortcuts import render, redirect
from django.views import View
from django.db.models import Q, Count

from backend import models, forms

from pprint import pprint

import json
from .helpers import get_chart_data, get_list_periods, get_content_table, split_list, get_content_comparison, get_table_summarizer, get_highlight_dashboard_items, get_subjects_lists
from django.core.serializers.json import DjangoJSONEncoder
from django.http import JsonResponse, HttpResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from operator import itemgetter
class HomeAppClassView(View):

    def get(self, request):

        # Subject Data
        subjs_data = get_subjects_lists(grouping=True)
        cards = get_subjects_lists(grouping=False)
        mid = len(cards) // 2
        cards = [cards[:mid], cards[mid:]]

        # Publikasi Data
        publications = models.BackendPublicationsModel.objects.order_by('-release', 'title').values()
        infographics = models.BackendInfographicsModel.objects.order_by('-created_at').values()
        videographs = models.BackendVideoGraphicsModel.objects.order_by('-created_at').values()
        news = models.BackendStatsNewsModel.objects.filter(show_state = '1').values()
        count_media_stats = len(publications) + len(videographs) + len(videographs) + len(news)
        services = models.BackendDataConsultModel.objects.values()

        count_services = len(services)
        count_stats = len(models.BackendContentIndicatorsModel.objects.values('indicator_id', 'indicator_id__name', 'indicator_id__updated_at', 'indicator_id__time_period_id__name').distinct())
        dev_stats = len(models.BackendContentIndicatorsModel.objects.filter(~Q(indicator_id__level_data = '0')).values('indicator_id', 'indicator_id__name', 'indicator_id__updated_at', 'indicator_id__time_period_id__name', 'indicator_id__stat_category').distinct())

        context = {
            'title' : 'SDM | Satu Data Muna',
            'subjects' : subjs_data,
            'count_stats' : '{:,}'.format(count_stats).replace(',','.'), 
            'counts_dev' : '{:,}'.format(dev_stats).replace(',','.'),
            'counts_dev' : '{:,}'.format(dev_stats).replace(',','.'),
            'count_media_stats': '{:,}'.format(count_media_stats).replace(',','.'),
            'count_services' : '{:,}'.format(count_services).replace(',','.'),
            'cards' : cards,
            'publications' : publications[:16],
            'infographcs' : infographics[:16],
            'videographs': videographs[:16],
            'items_summarize' : get_highlight_dashboard_items(),
        }
        
        # return render(request, 'app/index.html', context)
        return render(request, 'app/app_new.html', context)

class HomeDataConsultClassView(View):

    def post(self, request):

        is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'
        if is_ajax:
            if request.method == 'POST':

                form = forms.BackendDataConsultForm(request.POST)

                if form.is_valid():
                    form.save()
                    return JsonResponse({"status": 'success'}, status=200)
                else:
                    return JsonResponse({"status": 'failed', "error": form.errors}, status=400)

        return JsonResponse({'status': 'Invalid request'}, status=400)

class HomeDataTraceClassView(View):

    def post(self, request):
        
        data = self._datatables(request)
        return HttpResponse(json.dumps(data, cls=DjangoJSONEncoder), content_type='application/json')
		
    def _datatables(self, request):

        # Define default column for ordering first request
        def_col = 'indicator_id__name' 

        datatables = request.POST
        # Get Draw
        draw = int(datatables.get('draw'))
        start = int(datatables.get('start'))
        
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
            Q(item_row=None)
        ).values('indicator_id', 'year', 'item_period').distinct()

        id_def_data = list(model.order_by(def_col).values_list('indicator_id', 'year', 'item_period').distinct())
        id_def_data = [list((idx+1, ) + id_def_data[idx]) for idx in range(len(id_def_data))]
        
        records_total = model.count()
        records_filtered = records_total
        if datatables.get('search_data'):

            search = datatables.get('search_data')
            model = models.BackendContentIndicatorsModel.objects.filter(
                Q(indicator_id__subject_id__name__icontains=search) |
                Q(indicator_id__name__icontains=search) |
                Q(indicator_id__time_period_id__name__icontains=search)|
                Q(created_at__icontains=search)|
                Q(item_period__icontains=search)|
                Q(year__icontains=search)
            ).exclude(
            Q(indicator_id=None) |
            Q(year=None) |
            Q(item_period=None) |
            Q(item_row=None)).values('indicator_id', 'year', 'item_period').distinct()

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
            obj_dt = models.BackendContentIndicatorsModel.objects.filter(indicator_id = obj['indicator_id'], year=obj['year'], item_period=obj['item_period']).first()
            obj_period = models.BackendPeriodNameItemsModel.objects.filter(pk = obj_dt.item_period).first()
            data.append(
            {
                'no': [x for x in id_def_data if obj_dt.indicator_id.id == x[1] and obj_dt.year == x[2] and obj_dt.item_period == x[3]][0][0],
                'indicator_id__name': obj_dt.indicator_id.name,
                'indicator_id__subject_id__name': obj_dt.indicator_id.subject_id.name,
                'indicator_id__time_period_id__name': f'{obj_period.item_period} {obj_dt.year}',
                'created_at' : obj_dt.created_at.strftime('%d %b %Y'),
            })
            
        return {    
            'draw': draw,
            'recordsTotal': records_total,
            'recordsFiltered': records_filtered,
            'data': data,
        }


class SearchEngineClassView(View):
    def get(self,request):
        context = {
            'title' : 'Kemiskinan | Telusuri Data'
        }

        return render(request, 'app/search_app.html', context)

class StatisticsTablesClassView(View):
    def get(self,request):

        model = models.BackendSubjectsModel.objects.filter(show_state = '1').order_by('subject_group', 'name')

        subjectItems = []
        for item in model:

            qry = models.BackendContentIndicatorsModel.objects.values('indicator_id','indicator_id__subject_id').filter(indicator_id__subject_id = str(item.pk)).distinct()

            check_exist = next((index for (index, d) in enumerate(subjectItems) if d["groups"] == item.get_subject_group_display()), None)
            if check_exist is None:
                subjectItems.append({
                    "groups"    : item.get_subject_group_display(),
                    "items"     : [
                        {
                            'id' : item.id,
                            'name' : item.name if len(item.name) <= 20 else f'{item.name[:20]}...',
                            'count' : qry.count() if qry.exists() else 0
                        }
                    ]
                })
            else:
                subjectItems[check_exist]['items'].append(
                    {
                        'id' : item.id,
                        'name' : item.name if len(item.name) <= 20 else f'{item.name[:20]}...',
                        'count' : qry.count() if qry.exists() else 0
                    }
                )

        context = {
            'title' : 'Kemiskinan | Tabel Statistik',
            'subjects' : subjectItems
        }
        
        return render(request, 'app/statistics.html', context)

class StatisticsDataTablesClassView(View):
    
    def post(self, request):
        
        data = self._datatables(request)
        return HttpResponse(json.dumps(data, cls=DjangoJSONEncoder), content_type='application/json')
		
    def _datatables(self, request):

        # Define default column for ordering first request
        def_col = 'indicator_id__name' 

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
        if datatables.get('subject'):
            model = model.filter(indicator_id__subject_id = datatables.get('subject'))

        model = model.exclude(
            Q(indicator_id=None) |
            Q(year=None) |
            Q(item_period=None) |
            Q(item_row=None)
        ).values('indicator_id', 'indicator_id__name', 'indicator_id__updated_at', 'indicator_id__time_period_id__name').distinct()

        id_def_data = list(model.order_by(def_col).values_list('indicator_id', 'indicator_id__name', 'indicator_id__updated_at', 'indicator_id__time_period_id__name').distinct())
        id_def_data = [list((idx+1, ) + id_def_data[idx]) for idx in range(len(id_def_data))]

        records_total = model.count()
        records_filtered = records_total
        
        if datatables.get('search-box'):
            search = datatables.get('search-box')
            model = models.BackendContentIndicatorsModel.objects.filter(
                Q(indicator_id__name__icontains=search) |
                Q(indicator_id__time_period_id__name__icontains=search)|
                Q(indicator_id__updated_at__icontains=search)
            )
            if datatables.get('subject'):
                model = model.filter(indicator_id__subject_id = datatables.get('subject'))
            
            model = model.exclude(
                Q(indicator_id=None) |
                Q(year=None) |
                Q(item_period=None) |
                Q(item_row=None)
            ).values('indicator_id', 'indicator_id__name', 'indicator_id__updated_at', 'indicator_id__time_period_id__name').distinct()

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
            qry = models.BackendIndicatorsModel.objects.filter(pk=obj['indicator_id']).first().col_group_id
            href = f'{reverse_lazy("app:statistics-app-preview")}?indicator={obj["indicator_id"]}' if qry is not None else f'{reverse_lazy("app:statistics-app-nocols")}?indicator={obj["indicator_id"]}'
            name = f'{obj["indicator_id__name"][:80]}..' if len(obj["indicator_id__name"]) > 80 else obj["indicator_id__name"]
            data.append(
            {
                'no': [x for x in id_def_data if obj['indicator_id'] == x[1]][0][0],
                'indicator_id__name': f'<a href="{href}" class="text-secondary" title="{obj["indicator_id__name"]}">{name}</a>' ,
                'indicator_id__time_period_id__name': obj['indicator_id__time_period_id__name'],
                'indicator_id__updated_at' : obj['indicator_id__updated_at'].strftime('%d %b %Y'),
            })

        return {    
            'draw': draw,
            'recordsTotal': records_total,
            'recordsFiltered': records_filtered,
            'data': data,
        }

class StatisticDetailNoColsTableClassView(View):

    def get(self, request):
        if request.GET.get('indicator'):
            indicator_id = request.GET.get('indicator')
            model = models.BackendIndicatorsModel.objects.filter(pk=indicator_id)
            if model.exists():
                model = model.first()
                
                # Cek baris apakah dummy or not
                have_rows = False if model.row_group_id.row_items.first().order_num == 99 else True
                data_meanings = models.BackendIndicatorsMeaningModel.objects.filter(indicator_id=indicator_id).order_by('year', 'item_period').values()
                model_data = models.BackendContentIndicatorsModel.objects.filter(indicator_id=indicator_id)
                model_data_period = model_data.order_by('year', 'item_period').values('year', 'item_period').distinct()
                
                list_periods = get_list_periods(model_data_period, request.GET.getlist('data'))
                data_content_table = get_content_table(indicator_id, request.GET.getlist('data'))
                data_summarize_table = get_table_summarizer(indicator_id, request.GET.getlist('data'))
                chart_data = get_chart_data(data_content_table, model.get_summarize_status_display(), model.unit_id.is_agg == '1', model.unit_id.is_viz, False)
                
                data_comparisons = []
                data_compare_req = []
                chart_data_compare = []
                data_comparisons_title = ''
                comp_in_years = True
                if request.GET.get('compare_by'):
                    data_compare_req = request.GET.get('compare_by').split('-')
                    data_comparisons = get_content_table(indicator_id, data_compare_req)
                    chart_data_compare = get_chart_data(data_comparisons, model.get_summarize_status_display(), model.unit_id.is_agg == '1', model.unit_id.is_viz, False)
                    data_comparisons = get_content_comparison(data_comparisons)

                    first_year, first_period = data_compare_req[0].split('_')
                    second_year, second_period = data_compare_req[1].split('_')
                    data_comparisons_title = f'Perbandingan {model.name} ({model.unit_id.name}), {models.BackendPeriodNameItemsModel.objects.filter(pk=first_period).first().item_period} ({first_year}) - {models.BackendPeriodNameItemsModel.objects.filter(pk=second_period).first().item_period} ({second_year})'
                    comp_in_years = first_year == second_year

                data_meanings_ = []
                for dt in data_meanings:
                    check_exist = next((index for (index, d) in enumerate(data_meanings_) if d['year'] == dt['year']), None)
                    context = {'item_period' : models.BackendPeriodNameItemsModel.objects.filter(pk=dt['item_period']).first().item_period, 'context' : dt['context']}
                    if check_exist is not None:
                        data_meanings_[check_exist]['items'].append(context)
                    else:
                        data_meanings_.append({
                            'year' : dt['year'],
                            'items' : [context]
                        })

                dt = data_content_table[0]
                count_period = len(dt['items'][0]['items'])
                count_cols = len(dt['items'][0]['items'][0]['items'])
                col_span = count_period * count_cols
                
                context = {
                    'title' : model.name,
                    'table' : model,
                    'have_rows': have_rows,
                    'table_last_updated' : model_data.order_by('-updated_at').first().updated_at,
                    'data_contents' : data_content_table,
                    'is_year' : True if model.col_group_id_id is None and len(list_periods[0]['periods'][0]['name']) == 0 else False,
                    'data_meanings' : data_meanings_,
                    'periods' : list_periods,
                    'col_span' : col_span,
                    'chart_data': chart_data,
                    'range_period' : f"Tahun {list_periods[0]['year']} s.d. {list_periods[-1]['year']}", 
                    'data_summarize' : data_summarize_table,
                    'data_comparisons' : data_comparisons,
                    'comp_in_years' : comp_in_years,
                    'data_comparisons_title' : data_comparisons_title,
                    'data_compare_req' : data_compare_req,
                    'chart_data_compare' : chart_data_compare
                }

                return render(request, 'app/statistics_preview_nocols.html', context)
            else:
                return redirect('app:statistics-app-nocols')
        else:
            return redirect('app:statistics-app-nocols')
        
class StatisticDetailTableClassView(View):

    def get(self, request):

        if request.GET.get('indicator'):
            indicator_id = request.GET.get('indicator')

            model = models.BackendIndicatorsModel.objects.filter(pk=indicator_id)
            if model.exists():
                model = model.first()
                data_meanings = models.BackendIndicatorsMeaningModel.objects.filter(indicator_id=indicator_id).order_by('year', 'item_period').values()
                model_data = models.BackendContentIndicatorsModel.objects.filter(indicator_id=indicator_id)
                model_data_period = model_data.order_by('year', 'item_period').values('year', 'item_period').distinct()
                
                # List Periods
                have_rows = False if model.row_group_id.row_items.first().order_num == 99 else True
                list_periods = get_list_periods(model_data_period, request.GET.getlist('data'))
                data_content_table = get_content_table(indicator_id, request.GET.getlist('data'))
                data_summarize_table = get_table_summarizer(indicator_id, request.GET.getlist('data'))
                chart_data = get_chart_data(data_content_table, model.get_summarize_status_display(), model.unit_id.is_agg == '1', model.unit_id.is_viz, True)
                chart_data['data_rows'] = [dt['row_name'] for dt in data_content_table] * len(list_periods)

                data_comparisons, data_compare_req, chart_data_compare = [], [], []
                data_comparisons_title = ''
                comp_in_years = True
                if request.GET.get('compare_by'):
                    data_compare_req = request.GET.get('compare_by').split('-')
                    data_comparisons = get_content_table(indicator_id, data_compare_req)
                    chart_data_compare = get_chart_data(data_comparisons, model.get_summarize_status_display(), model.unit_id.is_agg == '1', model.unit_id.is_viz, True)
                    chart_data_compare['data_rows'] = [dt['row_name'] for dt in data_comparisons] * len(list_periods)
                    data_comparisons = get_content_comparison(data_comparisons)

                    first_year, first_period = data_compare_req[0].split('_')
                    second_year, second_period = data_compare_req[1].split('_')
                    data_comparisons_title = f'Perbandingan {model.name} ({model.unit_id.name}), {models.BackendPeriodNameItemsModel.objects.filter(pk=first_period).first().item_period} ({first_year}) - {models.BackendPeriodNameItemsModel.objects.filter(pk=second_period).first().item_period} ({second_year})'
                    comp_in_years = first_year == second_year

                data_meanings_ = []
                for dt in data_meanings:
                    check_exist = next((index for (index, d) in enumerate(data_meanings_) if d['year'] == dt['year']), None)
                    context = {'item_period' : models.BackendPeriodNameItemsModel.objects.filter(pk=dt['item_period']).first().item_period, 'context' : dt['context']}
                    if check_exist is not None:
                        data_meanings_[check_exist]['items'].append(context)
                    else:
                        data_meanings_.append({
                            'year' : dt['year'],
                            'items' : [context]
                        })

                # Cols Data
                dt = data_content_table[0]
                count_period = len(dt['items'][0]['items'])
                count_cols = len(dt['items'][0]['items'][0]['items'])
                col_span = count_period * count_cols

                context = {
                    'title' : model.name,
                    'table' : model,
                    'have_rows' : have_rows,
                    'table_last_updated' : model_data.order_by('-updated_at').first().updated_at,
                    'data_contents' : data_content_table,
                    'data_meanings' : data_meanings_,
                    'range_period' : f"Tahun {list_periods[0]['year']} s.d. {list_periods[-1]['year']}", 
                    'data_summarize' : data_summarize_table,
                    'periods' : list_periods,
                    'is_year' : True if len(list_periods[0]['periods'][0]['name']) == 0 else False,
                    'col_span' : col_span,
                    'chart_data': chart_data,
                    'data_comparisons' : data_comparisons,
                    'data_comparisons_title' : data_comparisons_title,
                    'comp_in_years': comp_in_years,
                    'data_compare_req' : data_compare_req,
                    'chart_data_compare' : chart_data_compare
                }

                return render(request, 'app/statistics_preview.html', context)
            else:
                return redirect('app:statistics-app')
        else:
            return redirect('app:statistics-app')


class DataRequestsClassView(View):

    def get(self,request):
        context = {
            'title' : 'Konsultasi Data Statistik'
        }

        return render(request, 'app/data_request.html', context) 


class DataRequestPreviewClassView(View):

    def get(self,request):
        
        context = {
            'title' : 'Konsultasi Data Statistik',
        }

        return render(request, 'app/data_request_preview.html', context) 
    
class DashboardAppClassView(View):
    pass


class PublicationClassView(View):

    def get(self,request):
        context = {
            'title' : 'Publikasi Data Statistik'
        }

        return render(request, 'app/publications.html', context) 



class PublicationPreviewClassView(View):

    def get(self,request):
        context = {
            'title' : 'Publikasi Data Statistik'
        }

        return render(request, 'app/publication_preview.html', context) 


class InfographicsClassView(View):

    def get(self,request):
        context = {
            'title' : 'Infografis Statistik'
        }

        return render(request, 'app/infographics.html', context)

class InfographicPreviewClassView(View):

    def get(self,request):
        context = {
            'title' : 'Publikasi Data Statistik'
        }

        return render(request, 'app/infographic_preview.html', context)
    

class VideographicsClassView(View):

    def get(self,request):
        context = {
            'title' : 'Videografis Statistik'
        }

        return render(request, 'app/videographics.html', context)


class VideographicPreviewClassView(View):

    def get(self,request):
        context = {
            'title' : 'Publikasi Data Statistik'
        }

        return render(request, 'app/videographic_preview.html', context)

class StrategicDataClassView(View):

    def get(self,request):
        # Program Masih cacat
        model = models.BackendIndicatorsModel.objects.filter(~Q(level_data=0)).order_by('time_period_id__name', 'name')

        datasets = []
        for dt in model:

            table_content = models.BackendContentIndicatorsModel.objects.filter(indicator_id = dt.pk).order_by('-updated_at')
            if table_content.exists():

                group = dt.time_period_id.name
                periode_basic = []
                # NOTES: NANTI MASUKIN AGGREGATENYA APAKAH PAKAI SUM, RATA-RATA. ATAU PERSEN. Defalt ini kan masih pakai SUM

                if dt.unit_id.is_agg == '0': # Tidak dapat diagregatkan
                    continue
                # harus dicek dulu, klo dia gaada kolom atau langsung series, maka gaperlu liat is_agg != '0'

                qry_content = get_content_table(indicator_id = dt.pk, force_agg = 'sum')
                list_values = []
                for rows in qry_content:
                    for years in rows['items']:
                        for periods in years['items']:
                            period_name = f"{periods['item_period']} {years['year']}"
                            period_name_ = f"{periods['order_num']}_{periods['item_period']}_{years['year']}"

                            if period_name_ not in periode_basic:
                                periode_basic.append(period_name_)

                            for cols in periods['items']:
                                if cols['item_char'] == 'Total':

                                    check_val = next((idx for (idx, d) in enumerate(list_values) if d['period'] == period_name), None)
                                    if check_val is not None:
                                        list_values[check_val]['value'].append(cols['value'])
                                    else:
                                        list_values.append(
                                            {
                                                'period' : period_name,
                                                'value' : [cols['value']]
                                            }
                                        )
                
                for dt_ in list_values:
                    dt_['value'] = round(float(sum(dt_['value'])), dt.decimal_point)

                items_group = {}
                items_group['id'] = dt.pk
                items_group['data'] = f'{dt.name} ({dt.unit_id.name})'
                items_group['data_items'] = list_values
                items_group['last_updated'] = table_content.first().updated_at
                items_group['href'] = f'{reverse_lazy("app:statistics-app-preview")}?indicator={dt.pk}' if dt.col_group_id is not None else  f'{reverse_lazy("app:statistics-app-nocols")}?indicator={dt.pk}'
                
                check_group = next((idx for (idx, d) in enumerate(datasets) if d["group"] == group), None)

                if check_group is None:
                    datasets.append ({
                        'group' : group,
                        'period_basic' : periode_basic,
                        'items_group' : [items_group]
                    })
                else:
                        for period_ in periode_basic:
                            if period_ not in datasets[check_group]['period_basic']:
                                datasets[check_group]['period_basic'].append(period_)

                        datasets[check_group]['items_group'].append(items_group)

        for idx, dt in enumerate(datasets):

            # Order Period Basic
            orders = [item_dt.split('_') for item_dt in dt['period_basic']]
            orders = sorted(orders, key = lambda x: (x[2], x[0]))
            orders = [f"{order[1]} {order[2]}" for order in orders]

            datasets[idx]['period_basic'] = orders
            datasets[idx]['items_group'] = sorted(dt['items_group'], key=itemgetter('last_updated'), reverse=True) 

        src_colls = []
        for src in list(model.values_list('source', flat=True)):
            check = next((idx for (idx, d) in enumerate(src_colls) if d.lower().replace(" ", "") == src.lower().replace(" ", "")), None)
            if check is None:
                src_colls.append(src)

        context = {
            'title' : 'Indikator Data Strategis',
            'datasets' : datasets,
            'sources' : src_colls
        }

        return render(request, 'app/strategic_data.html', context)
    