from django.shortcuts import render
from random import sample

from .models import Liste

# Create your views here.

def index(request):
    """Index page"""
    return render(request, 'vokabel_trainer/index.html')

def listen(request):
    """Index aller Vokabellisten"""
    listen = Liste.objects.order_by('date_added')
    context = {'listen': listen}
    return render(request, 'vokabel_trainer/listen.html', context)

def liste(request, liste_id):
    """Vokabelliste"""
    liste=Liste.objects.get(id=liste_id)
    vokabeln=liste.vokabel_set.order_by('-date_added')
    context={'liste':liste, 'vokabeln':vokabeln}
    return render(request, 'vokabel_trainer/liste.html', context)

def abfragen(request, liste_id):
    """Erstellt eine Abfrage zu einer Liste"""
    liste=Liste.objects.get(id=liste_id)
    vokabeln=liste.vokabel_set.all()
    anzahl_vokabeln=min(len(vokabeln), 3)

    abfragen=sample(list(vokabeln),k=anzahl_vokabeln)
    context = {'liste': liste, 'abfragen': abfragen}
    return render(request, 'vokabel_trainer/abfragen.html', context)
