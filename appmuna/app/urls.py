from django.urls import path
from . import views

app_name = 'app'

urlpatterns = [
    path('app/', views.HomeAppClassView.as_view(), name='home-app'),
    path('app/data-consult', views.HomeDataConsultClassView.as_view(), name='data-consult-app')
    
]
