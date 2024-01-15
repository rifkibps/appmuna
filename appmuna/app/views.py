from django.shortcuts import render
from django.views import View


class HomeAppClassView(View):

    def get(self, request):
        context = {
            'title' : 'SDM | Satu Data Muna'
        }
        return render(request, 'app/index.html', context)

class DashboardAppClassView(View):
    print('hello world')