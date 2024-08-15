from django.shortcuts import render
from django.views import View
from app.helpers import get_highlight_dashboard_items
from backend import models as app_model 
from . import models
class HomePageClassView(View):
    def get(self, request):

        pubs = app_model.BackendInfographicsModel.objects.filter(show_state = '1').order_by('-updated_at').values()
        faq = models.FAQModels.objects.order_by('-created_at').values()
        context = {
            'title' : 'Home Page',
            'pubs' : pubs,
            'faq' : faq,
            'items_summarize' : get_highlight_dashboard_items()
        }
        return render(request, 'homepage/index.html', context)

