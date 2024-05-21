from django.urls import path
from . import views

app_name = 'app'

urlpatterns = [
    path('app/', views.HomeAppClassView.as_view(), name='home-app'),
    path('app/data-consult', views.HomeDataConsultClassView.as_view(), name='data-consult-app'),
    path('app/data-tracing', views.HomeDataTraceClassView.as_view(), name='data-tracing-app'),

    path('app/statistics', views.StatisticsTablesClassView.as_view(), name='statistics-app'),
    path('app/statistics/data', views.StatisticsDataTablesClassView.as_view(), name='statistics-app-data'),

    path('app/statistics/preview', views.StatisticDetailTableClassView.as_view(), name='statistics-app-preview'),
    path('app/development-data', views.DevelopmenDataClassView.as_view(), name='dev-app'),
    path('app/strategic-data', views.StrategicDataClassView.as_view(), name='strategic-app'),
    

    path('app/service', views.DataRequestsClassView.as_view(), name='data-request-app'),
    path('app/service/consult-data/preview', views.DataRequestPreviewClassView.as_view(), name='data-request-preview'),
    
    path('app/media/publications', views.PublicationClassView.as_view(), name='publications'),
    path('app/media/publications/preview', views.PublicationPreviewClassView.as_view(), name='publication-preview'),
    path('app/media/infographics', views.InfographicsClassView.as_view(), name='infographs'),
    path('app/media/infographics/preview', views.InfographicPreviewClassView.as_view(), name='infograph-preview'),


    path('app/media/videographics', views.VideographicsClassView.as_view(), name='videographics'),
    path('app/media/videographic/preview', views.VideographicPreviewClassView.as_view(), name='videographic-preview'),

    
    path('app/search', views.SearchEngineClassView.as_view(), name='search-app')
    
]
