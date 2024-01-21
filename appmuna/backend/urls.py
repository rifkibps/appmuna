from django.urls import path
from . import views

app_name = 'backend'

urlpatterns = [
    path('backend/', views.BackendAppClassView.as_view(), name='backend'),

    path('backend/units', views.BackendUnitsClassView.as_view(), name='backend-units'),
    path('backend/units/json', views.BackendUnitsJsonClassView.as_view(), name='backend-units-json'),
    path('backend/units/delete', views.BackendUnitDeleteClassView.as_view(), name='backend-units-delete'),
    path('backend/units/multiple-delete', views.BackendUnitMultipleDeleteClassView.as_view(), name='backend-units-multiple-delete'),
    path('backend/units/detail', views.BackendUnitDetailClassView.as_view(), name='backend-units-detail'),
    path('backend/units/export', views.BackendUnitsExportClassView.as_view(), name='backend-units-export'),

    path('backend/periods', views.BackendPeriodsItemsClassView.as_view(), name='backend-periods'),
    path('backend/periods/json', views.BackendPeriodsJsonClassView.as_view(), name='backend-periods-json'),
    path('backend/periods/delete', views.BackendPeriodsdDeleteClassView.as_view(), name='backend-periods-delete'),
    path('backend/periods/detail', views.BackendPeriodDetailClassView.as_view(), name='backend-periods-detail'),
    
    
    path('backend/rows', views.BackendRowsItemsClassView.as_view(), name='backend-rows'),
    path('backend/columns', views.BackendCharsItemsClassView.as_view(), name='backend-cols'),
    path('backend/subjects', views.BackendCharsItemsClassView.as_view(), name='backend-subjs'),
    path('backend/indicators', views.BackendIndicatorsClassView.as_view(), name='backend-indicators'),
    path('backend/content', views.BackendContentIndicatorsClassView.as_view(), name='backend-content-tables'),    
]
