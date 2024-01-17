from django.urls import path
from . import views

app_name = 'backend'

urlpatterns = [
    path('backend/', views.BackendAppClassView.as_view(), name='backend'),
    path('backend/units', views.BackendUnitsClassView.as_view(), name='backend-units'),
    path('backend/periods', views.BackendPeriodsItemsClassView.as_view(), name='backend-periods')
]
