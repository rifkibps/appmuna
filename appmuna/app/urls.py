from django.urls import path
from . import views

app_name = 'app'

urlpatterns = [
    path('app/', views.HomeAppClassView.as_view(), name='home-app'),
    path('app/data-consult', views.HomeDataConsultClassView.as_view(), name='data-consult-app'),
    path('app/data-tracing', views.HomeDataTraceClassView.as_view(), name='data-tracing-app'),


    path('app/statistics', views.StatisticsTablesClassView.as_view(), name='statistics-app'),
    path('app/statistics/preview', views.StatisticDetailTableClassView.as_view(), name='statistics-app'),
    path('app/service', views.DataRequestsClassView.as_view(), name='data-request-app'),
    path('app/service/consult-data/preview', views.DataRequestPreviewClassView.as_view(), name='data-request-preview'),
    
    
    path('app/search', views.SearchEngineClassView.as_view(), name='search-app')
    
]
