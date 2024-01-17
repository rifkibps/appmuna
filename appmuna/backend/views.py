from django.shortcuts import render
from django.views import View


class BackendAppClassView(View):

    def get(self, request):
        context = {
            'title' : 'Backend | Portal Administrator'
        }
        return render(request, 'backend/index.html', context)


class BackendUnitsClassView(View):
    def get(self, request):
        context = {
            'title' : 'Backend | Satuan Data'
        }
        return render(request, 'backend/units.html', context)


class BackendPeriodsItemsClassView(View):
    def get(self, request):
        context = {
            'title' : 'Backend | Satuan Data'
        }
        return render(request, 'backend/periods.html', context)