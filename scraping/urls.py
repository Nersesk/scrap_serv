from django.urls import path
from .views import home_view,list_view
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = [
    path('',home_view,name='home'),
    path('list/',list_view,name='list'),
]

urlpatterns += staticfiles_urlpatterns()