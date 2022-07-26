from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('business', views.business, name='business'),
]
