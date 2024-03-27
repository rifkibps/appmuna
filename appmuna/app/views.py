from django.shortcuts import render
from django.views import View
from backend import models

from app.helpers import split_list
from pprint import pprint

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
                    'desc' : f'{' '.join(abstract[:10])} ...', # Maks 71 chars
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
                    'desc' : f'{' '.join(desc[:10])} ...', # Maks 71 chars
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
            val['content']  =  f'{' '.join(content[:20])} ...'

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

class DashboardAppClassView(View):
    print('hello world')
    print('Ini perubahan dari master')