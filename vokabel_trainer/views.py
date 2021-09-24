from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from random import sample
from datetime import datetime

from .models import Liste, Abfrage
from .forms import ListeForm, VokabelForm, AbfrageForm

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
    form=AbfrageForm()
    liste=Liste.objects.get(id=liste_id)
    vokabeln=liste.vokabel_set.order_by('-date_added')
    abfragen=liste.abfrage_set.all()
    context={'liste':liste, 'vokabeln':vokabeln, 'abfragen':abfragen,'form':form}
    return render(request, 'vokabel_trainer/liste.html', context)

def neue_liste(request):
    """Erstellt neue Vokabelliste"""
    if request.method != 'POST':
        form=ListeForm()
    else:
        form=ListeForm(data=request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('vokabel_trainer:listen'))

    context ={'form':form}
    return render(request, 'vokabel_trainer/neue_liste.html', context)

def neue_vokabel(request,liste_id):
    """Erstellt neue Vokabel"""
    liste=Liste.objects.get(id=liste_id)
    vokabeln=liste.vokabel_set.order_by('deutsch')

    if request.method != 'POST':
        form=VokabelForm()
    else:
        form=VokabelForm(data=request.POST)
        if form.is_valid():
            neue_vokabel=form.save(commit=False)
            neue_vokabel.liste=liste
            neue_vokabel.save()
            return HttpResponseRedirect(reverse('vokabel_trainer:liste',args=[liste_id]))

    context={'liste':liste,'form':form, 'vokabeln':vokabeln}

    return render(request, 'vokabel_trainer/neue_vokabel.html', context)

def abfrage(request,abfrage_id):
    """Zeigt Abfrage"""
    abfrage=Abfrage.objects.get(id=abfrage_id)
    liste=abfrage.liste
    vokabeln=abfrage.vokabeln.all()

    context={'abfrage':abfrage,'liste':liste,'vokabeln':vokabeln}
    return render(request,'vokabel_trainer/abfrage.html', context)

def neue_abfrage(request,liste_id):
    """Erstellt neue Abfrage"""
    liste=Liste.objects.get(id=liste_id)
    vokabeln=list(liste.vokabel_set.all())
    vokabeln=sample(vokabeln, min(5, len(vokabeln)))

    neue_abfrage=Abfrage.objects.create(
        liste=liste,
        date_added=datetime.now()
    )
    neue_abfrage.vokabeln.set(vokabeln)
    return HttpResponseRedirect(reverse('vokabel_trainer:abfrage',args=[neue_abfrage.id]))
