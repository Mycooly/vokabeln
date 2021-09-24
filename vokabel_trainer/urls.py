"""Defines url-patterns for vokabel_trainer"""

from django.conf.urls import url

from . import views

urlpatterns=[
    url(r'^$',views.index, name='index'),

    url(r'^listen/$', views.listen, name='listen'),
    url(r'listen/(?P<liste_id>\d+)/$', views.liste, name='liste'),
    url(r'^neue_liste/$', views.neue_liste, name='neue_liste'),
    url(r'^neue_vokabel/(?P<liste_id>\d+)/$', views.neue_vokabel, name='neue_vokabel'),

    url(r'^abfrage/(?P<abfrage_id>\d+)/', views.abfrage, name='abfrage'),
    url(r'^neue_abfrage/(?P<liste_id>\d+)/', views.neue_abfrage, name='neue_abfrage')


]