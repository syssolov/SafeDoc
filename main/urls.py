from django.urls import path
from .views import *
from django.shortcuts import render


urlpatterns = [
	path('', IndexPageView.as_view(), name='index'),
	path('storages/', StoragePageView.as_view(), name='storages'),
	path('docs/', DocPageView.as_view(), name='docs'),
	path('about/', AboutPageView.as_view(), name='about'),
	path('history/', HistoryPageView.as_view(), name='history'),
]