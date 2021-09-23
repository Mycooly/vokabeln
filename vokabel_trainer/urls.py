"""Defines url-patterns for vokabel_trainer"""

from django.conf.urls import url

from . import views

urlpatterns=[
    url(r'^$',views.index, name='index'),

    url(r'^listen/$', views.listen, name='listen'),
    url(r'listen/(?P<liste_id>\d+)/$', views.liste, name='liste'),

    url(r'^abfragen/(?P<liste_id>\d+)/$', views.abfragen, name='abfragen'),
]