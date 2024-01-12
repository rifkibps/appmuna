from django.shortcuts import render
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin


class HomePageClassView(View):
    def get(self, request):
        context = {
            'title' : 'Home Page'
        }
        return render(request, 'homepage/index.html', context)

