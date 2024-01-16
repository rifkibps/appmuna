from django.urls import path
from . import views

app_name = 'backend'

urlpatterns = [
    path('backend/', views.BackendAppClassView.as_view(), name='backend')
]
