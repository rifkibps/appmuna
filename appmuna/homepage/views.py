from django.shortcuts import render
from django.views import View
from app.helpers import get_highlight_dashboard_items

class HomePageClassView(View):
    def get(self, request):
        context = {
            'title' : 'Home Page',
            'items_summarize' : get_highlight_dashboard_items()
        }
        return render(request, 'homepage/index.html', context)

