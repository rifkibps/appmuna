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
    path('backend/periods/multiple-delete', views.BackendPeriodsMultipleDeleteClassView.as_view(), name='backend-periods-multiple-delete'),
    path('backend/periods/export', views.BackendPeriodsExportClassView.as_view(), name='backend-periods-export'),
    
    
    path('backend/rows', views.BackendRowsItemsClassView.as_view(), name='backend-rows'),
    path('backend/rows/json', views.BackendRowsJsonClassView.as_view(), name='backend-rows-json'),
    path('backend/rows/detail', views.BackendRowDetailClassView.as_view(), name='backend-row-detail'),
    path('backend/rows/delete', views.BackendRowDeleteClassView.as_view(), name='backend-row-delete'),
    path('backend/rows/multiple-delete', views.BackendRowsMultipleDeleteClassView.as_view(), name='backend-rows-multiple-delete'),
    path('backend/rows/export', views.BackendRowsExportClassView.as_view(), name='backend-rows-export'),


    path('backend/characteristics', views.BackendCharsClassView.as_view(), name='backend-chars'),
    path('backend/characteristics/json', views.BackendCharsJsonClassView.as_view(), name='backend-chars-json'),
    path('backend/characteristics/delete', views.BackendCharDeleteClassView.as_view(), name='backend-char-delete'),
    path('backend/characteristics/multiple-delete', views.BackendCharsMultipleDeleteClassView.as_view(), name='backend-chars-multiple-delete'),
    path('backend/characteristics/detail', views.BackendCharDetailClassView.as_view(), name='backend-char-detail'),
   

    path('backend/subjects', views.BackendSubjectsClassView.as_view(), name='backend-subjs'),
    path('backend/subjects/json', views.BackendSubjectsJsonClassView.as_view(), name='backend-subjs-json'),
    path('backend/subjects/delete', views.BackendSubjectDeleteClassView.as_view(), name='backend-subj-delete'),
    path('backend/subjects/multiple-delete', views.BackendSubjectsMultipleDeleteClassView.as_view(), name='backend-subjs-multiple-delete'),
    path('backend/subjects/switch', views.BackendSubjectSwitchStateClassView.as_view(), name='backend-subj-switch'),
    path('backend/subjects/detail', views.BackendSubjectDetailClassView.as_view(), name='backend-subj-detail'),
    path('backend/subjects/export', views.BackendSubjectsExportClassView.as_view(), name='backend-subjs-export'),
    

    path('backend/indicators', views.BackendIndicatorsClassView.as_view(), name='backend-indicators'),
    path('backend/indicators/json', views.BackendIndicatorsJsonClassView.as_view(), name='backend-indicators-json'),
    path('backend/indicators/switch', views.BackendIndicatorSwitchStateClassView.as_view(), name='backend-indicator-switch'),
    path('backend/indicators/detail', views.BackendIndicatorDetailClassView.as_view(), name='backend-indicator-detail'),
    path('backend/indicators/delete', views.BackendIndicatorDeleteClassView.as_view(), name='backend-indicator-delete'),
    path('backend/indicators/multiple-delete', views.BackendIndicatorsMultipleDeleteClassView.as_view(), name='backend-indicator-multiple-delete'),
    path('backend/indicators/export', views.BackendIndicatorsExportClassView.as_view(), name='backend-indicators-export'),
    

    path('backend/content', views.BackendContentClassView.as_view(), name='backend-content'),
    path('backend/content/manage/json', views.BackendContentJsonClassView.as_view(), name='backend-content-json'),
    path('backend/content/manage/delete', views.BackendContentDeleteClassView.as_view(), name='backend-content-delete'),
    path('backend/content/manage/multiple-delete', views.BackendContentMultipleDeleteClassView.as_view(), name='backend-content-multiple-delete'),
    path('backend/content/manage/export', views.BackendContentExportClassView.as_view(), name='backend-content-export'),

    path('backend/content/input/', views.BackendContentInputClassView.as_view(), name='backend-content-input'),
    path('backend/content/input/form', views.BackendContentInputFormClassView.as_view(), name='backend-content-input-form'),
    path('backend/content/input/submit', views.BackendContentInputFormSubmitClassView.as_view(), name='backend-content-input-submit')
]
