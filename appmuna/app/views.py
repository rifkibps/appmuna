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
          
        pubs = models.BackendPublicationsModel.objects.order_by('release', 'title')[:16]

        pubs_data_card = []

        pubs_data = split_list(pubs, 4)


        context = {
            'title' : 'SDM | Satu Data Muna',
            'subjects' : subjs_data,
            'cards' : card_data_pages,
            'pubs' : pubs
        }

        return render(request, 'app/index.html', context)

class DashboardAppClassView(View):
    print('hello world')
    print('Ini perubahan dari master')