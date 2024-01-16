from django.shortcuts import render
from django.views import View


class BackendAppClassView(View):

    def get(self, request):
        context = {
            'title' : 'Backend | Portal Administrator'
        }
        return render(request, 'backend/index.html', context)
