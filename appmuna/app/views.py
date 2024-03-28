from django.shortcuts import render
from django.views import View
from django.db.models import Q

from backend import models, forms

from app.helpers import split_list
from pprint import pprint

import json
from django.core.serializers.json import DjangoJSONEncoder
from django.http import JsonResponse, HttpResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

class HomeAppClassView(View):

    def get(self, request):

        subjs_data = []
        subjects = models.BackendSubjectsModel.objects.order_by('subject_group', 'name')

        for subj in subjects:
            check_exist = next((index for (index, d) in enumerate(subjs_data) if d["groups"] == subj.get_subject_group_display()), None)
            if check_exist is None:
                subjs_data.append({
                    "groups"    : subj.get_subject_group_display(),
                    "items"     : [
                        {
                            'id' : subj.id,
                            'item' : subj.name
                        }
                    ]
                })
            else:
                subjs_data[check_exist]['items'].append(
                    {
                        'id' : subj.id,
                        'item' : subj.name
                    }
                )
        
        card_data_pages = []

        card_data = split_list(subjects, 12)

        for idx, val in enumerate(card_data):
            dt = []
            for dt_val in val:
                dt.append({
                    'group' : dt_val.get_subject_group_display(),
                    'item' : dt_val.name,
                    'id' : dt_val.id
                })
            
            card_data_pages.append({
                'no' : idx,
                'items': dt
            })
          
        pubs = models.BackendPublicationsModel.objects.order_by('-release', 'title')
        pubs_data_card = []
        pubs_data = split_list(pubs[:16], 4)

        for idx, val in enumerate(pubs_data):
            dt = []
            for dt_val in val:

                abstract = list(dt_val.abstract.split(" ")) 
                dt.append({
                    'title' : dt_val.title,
                    'thumbnail' : dt_val.thumbnail,
                    'desc' : f"{' '.join(abstract[:10])} ...",
                    'id' : dt_val.id
                })
            
            pubs_data_card.append({
                'no' : idx,
                'items': dt
            })
          
        infographics = models.BackendInfographicsModel.objects.order_by('-created_at')
        infographs_data_card = []
        infographs_data = split_list(infographics[:16], 4)

        for idx, val in enumerate(infographs_data):
            dt = []
            for dt_val in val:

                desc = list(dt_val.desc.split(" ")) 
                dt.append({
                    'title' : dt_val.title,
                    'thumbnail' : dt_val.thumbnail,
                    'desc' : f"{' '.join(desc[:10])} ...", # Maks 71 chars
                    'id' : dt_val.id
                })
            
            infographs_data_card.append({
                'no' : idx,
                'items': dt
            })


        videographs = models.BackendVideoGraphicsModel.objects.order_by('-created_at')

        stats_news = models.BackendStatsNewsModel.objects.order_by('-created_at').values()[:4]
        for val in stats_news:
            content = list(val['content'].split(" ")) 
            val['content']  =  f"{' '.join(content[:20])} ..."

        stats_data = models.BackendIndicatorsModel.objects.order_by('created_at')[:4]
        stats_data_str = models.BackendIndicatorsModel.objects.filter(level_data = '1').order_by('created_at')[:4]
        stats_data_ikm = models.BackendIndicatorsModel.objects.filter(level_data = '2').order_by('created_at')[:4]

        context = {
            'title' : 'SDM | Satu Data Muna',
            'subjects' : subjs_data,
            'cards' : card_data_pages,
            'pubs' : pubs_data_card,
            'infographcs' : infographs_data_card,

            'stats_news' : stats_news,
            'pubs_data': pubs[:9],
            'infographs_data' : infographics[:8],
            'videographs_data' : videographs[:9],
            'stats_data' : stats_data,
            'stats_data_str' : stats_data_str,
            'stats_data_ikm' : stats_data_ikm,
        }

        return render(request, 'app/index.html', context)

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

class HomeDataTraceClassView(LoginRequiredMixin, View):

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
            Q(item_row=None)
        ).values('indicator_id', 'year', 'item_period').distinct()

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

            print(obj_period.item_period)
            data.append(
            {
                'no': [x for x in id_def_data if obj_dt.indicator_id.id == x[1] and obj_dt.year == x[2] and obj_dt.item_period == x[3]][0][0],
                'indicator_id__name': obj_dt.indicator_id.name,
                'indicator_id__subject_id__name': obj_dt.indicator_id.subject_id.name,
                'indicator_id__time_period_id__name': obj_period.item_period,
                'year': obj_dt.year,
                'item_period': obj_dt.item_period,
                'created_at' : obj_dt.created_at.strftime('%d %b %Y'),
            })
        return {    
            'draw': draw,
            'recordsTotal': records_total,
            'recordsFiltered': records_filtered,
            'data': data,
        }



class DashboardAppClassView(View):
    print('hello world')
    print('Ini perubahan dari master')