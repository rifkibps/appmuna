from django.shortcuts import render
from django.views import View
from backend import models

import math
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

        def partition(lst, size):
            for i in range(0, len(lst) // size):
                yield lst[i :: size]

        card_data = [subjects[x::12] for x in range(len(subjects)//12)]
        pprint(card_data)
        for idx, val in enumerate(card_data):
            print(idx)
            dt = []

            for dt_val in val:
                print(dt_val.name)
                # dt.append({
                #     'group' : dt_val.get_subject_group_display(),
                #     'item' : dt_val.name
                # })
            
            # card_data_pages.append({
            #     'no' : idx,
            #     'items': dt
            # })
          
        context = {
            'title' : 'SDM | Satu Data Muna',
            'subjects' : subjs_data,
            'cards' : card_data_pages
        }


        return render(request, 'app/index.html', context)

class DashboardAppClassView(View):
    print('hello world')
    print('Ini perubahan dari master')