"""Defines url-patterns for vokabel_trainer"""

from django.conf.urls import url

from . import views
from . import views_vokabel, views_liste, views_abfrage


# Definition der URLs

re = r'(?P<abfrage_id>\d+)/(?P<abfrage_nummer>\d+)/(?P<erster_versuch>[01])/(?P<anzahl_versuche>\d+)/(?P<tipp_nr>\d+)/$'

urlpatterns = [
    # Index
    url(r'^$', views.index, name='index'),

    # Listen
    url(r'^listen/$', views_liste.listen, name='listen'),
    url(r'listen/(?P<liste_id>\d+)/$', views_liste.liste, name='liste'),
    url(r'^neue_liste/$', views_liste.neue_liste, name='neue_liste'),
    url(r'^liste_bearbeiten/(?P<liste_id>\d+)/$', views_liste.liste_bearbeiten, name='liste_bearbeiten'),
    url(r'^liste_loeschen/(?P<liste_id>\d+)/$', views_liste.liste_loeschen, name='liste_loeschen'),

    # Grafik
    url(r'^population-chart/(?P<abfrage_id>\d+)/$', views_abfrage.population_chart, name='population-chart'),

    # Vokabeln
    url(r'^neue_vokabel/(?P<liste_id>\d+)/$', views_vokabel.neue_vokabel, name='neue_vokabel'),
    url(r'^vokabel_bearbeiten/(?P<vokabel_id>\d+)/$', views_vokabel.vokabel_bearbeiten, name='vokabel_bearbeiten'),
    url(r'^vokabel_loeschen/(?P<vokabel_id>\d+)/$', views_vokabel.vokabel_loeschen, name='vokabel_loeschen'),

    # Abfragen
    url(r'^abfrage/(?P<abfrage_id>\d+)/$', views_abfrage.abfrage, name='abfrage'),
    url(r'^neue_abfrage/(?P<liste_id>\d+)/$', views_abfrage.neue_abfrage, name='neue_abfrage'),
    url(r'^aktive_abfrage/' + re, views_abfrage.aktive_abfrage, name='aktive_abfrage'),
    url(r'^abfrage_abbrechen/(?P<abfrage_id>\d+)/$', views_abfrage.abfrage_abbrechen, name='abfrage_abbrechen'),
]
