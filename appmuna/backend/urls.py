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

    path('backend/content/input', views.BackendContentInputClassView.as_view(), name='backend-content-input'),
    path('backend/content/input/form', views.BackendContentInputFormClassView.as_view(), name='backend-content-input-form'),
    path('backend/content/input/delete', views.BackendContentDeleteClassView.as_view(), name='backend-content-delete'),
    path('backend/content/input/submit', views.BackendContentInputFormSubmitClassView.as_view(), name='backend-content-input-submit'),


    path('backend/statistic-news', views.BackendStatsNewsClassView.as_view(), name='backend-news'),
    path('backend/statistic-news/json', views.BackendStatsNewsJsonClassView.as_view(), name='backend-statnews-json'),
    path('backend/statistic-news/delete', views.BackendStatsNewsDeleteClassView.as_view(), name='backend-statnews-delete'),
    path('backend/statistic-news/detail', views.BackendStatsNewsDetailClassView.as_view(), name='backend-statnews-detail'),
    path('backend/statistic-news/switch', views.BackendStatsNewsSwitchStateClassView.as_view(), name='backend-statnews-switch'),
    path('backend/statistic-news/multiple-delete', views.BackendStatsNewsMultipleDeleteClassView.as_view(), name='backend-statnews-multiple-delete'),
    
    path('backend/infographics', views.BackendInfoGraphicsClassView.as_view(), name='backend-infographics'),
    path('backend/infographics/json', views.BackendInfoGraphicsJsonClassView.as_view(), name='backend-infographics-json'),
    path('backend/infographics/delete', views.BackendInfoGraphicDeleteClassView.as_view(), name='backend-infographics-delete'),
    path('backend/infographics/detail', views.BackendInfoGraphicDetailClassView.as_view(), name='backend-infographic-detail'),
    path('backend/infographics/switch', views.BackendInfoGraphicSwitchStateClassView.as_view(), name='backend-infographic-switch'),
    path('backend/infographics/multiple-delete', views.BackendInfoGraphicsSMultipleDeleteClassView.as_view(), name='backend-infographics-multiple-delete'),
  
    path('backend/videographics', views.BackendVideoGraphicsClassView.as_view(), name='backend-videographics'),
    path('backend/videographics/json', views.BackendVideoGraphicsJsonClassView.as_view(), name='backend-videographics-json'),
    path('backend/videographics/delete', views.BackendVideoGraphicDeleteClassView.as_view(), name='backend-videographic-delete'),
    path('backend/videographics/switch', views.BackendVideoGraphicSwitchStateClassView.as_view(), name='backend-videographic-switch'),
    path('backend/videographics/detail', views.BackendVideoGraphicDetailClassView.as_view(), name='backend-videographic-detail'),
    path('backend/videographics/multiple-delete', views.BackendVideoGraphicsMultipleDeleteClassView.as_view(), name='backend-videographic-multiple-delete'),
  
    path('backend/static-table', views.BackendContentStatisClassView.as_view(), name='backend-static-table'),
    path('backend/static-table/json', views.BackendContentStatisJsonClassView.as_view(), name='backend-static-json'),
    path('backend/static-table/delete', views.BackendContentStatisDeleteClassView.as_view(), name='backend-static-delete'),
    path('backend/static-table/switch', views.BackendContentStatisSwitchStateClassView.as_view(), name='backend-static-switch'),
    path('backend/static-table/detail', views.BackendContentStatisDetailClassView.as_view(), name='backend-static-detail'),
    path('backend/static-table/multiple-delete', views.BackendContentStatisMultipleDeleteClassView.as_view(), name='backend-static-multiple-delete'),

    path('backend/data-request', views.BackendDataRequestsClassView.as_view(), name='backend-data-request'),
    path('backend/data-request/json', views.BackendDataRequestsJsonClassView.as_view(), name='backend-request-json'),
    path('backend/data-request/switch', views.BackendDataRequestsSwitchClassView.as_view(), name='backend-request-switch'),
    path('backend/data-request/delete', views.BackendDataRequestDeleteClassView.as_view(), name='backend-request-delete'),
    path('backend/data-request/multiple-delete', views.BackendDataRequestsMultipleDeleteClassView.as_view(), name='backend-request-multiple-delete'),


    path('backend/publications', views.BackendPublicationsClassView.as_view(), name='backend-publications'),
    path('backend/publications/json', views.BackendPublicationsJsonClassView.as_view(), name='backend-publications-json'),
    path('backend/publications/switch', views.BackendPublicationSwitchClassView.as_view(), name='backend-publication-switch'),
    path('backend/publications/delete', views.BackendPublicationDeleteClassView.as_view(), name='backend-publication-delete'),
    path('backend/publications/multiple-delete', views.BackendPublicationMultipleDeleteClassView.as_view(), name='backend-publications-multiple-delete'),
    path('backend/publications/detail', views.BackendPublicationDetailClassView.as_view(), name='backend-publication-detail'),
    
]
