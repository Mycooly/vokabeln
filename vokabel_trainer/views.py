from django.shortcuts import render
from django.http import HttpResponseRedirect, Http404
from django.urls import reverse
from numpy.random import choice
from numpy import sum
from math import cos
from datetime import datetime

from .models import Liste, Abfrage
from .forms import ListeForm, VokabelForm, AbfrageForm, EingabeForm

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
    vokabeln=liste.vokabel_set.order_by('percentage')
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
    if request.method != 'POST':
        raise Http404
    else:
        liste=Liste.objects.get(id=liste_id)
        vokabeln=list(liste.vokabel_set.all())
        weights=[cos(vokabel.percentage) for vokabel in vokabeln]
        weights=weights/sum(weights)
        form=AbfrageForm(data=request.POST)
        vokabelzahl=int(form['vokabelzahl'].value())
        vokabeln=choice(vokabeln, size=min(vokabelzahl, len(vokabeln)), replace=False, p=weights)

        neue_abfrage=Abfrage.objects.create(
            liste=liste,
            date_added=datetime.now()
        )
        neue_abfrage.vokabeln.set(vokabeln)
        return HttpResponseRedirect(reverse('vokabel_trainer:abfrage',args=[neue_abfrage.id]))

def aktive_abfrage(request, abfrage_id, abfrage_nummer, erster_versuch):
    """Führt eine Abfrage durch"""
    abfrage=Abfrage.objects.get(id=abfrage_id)
    abfrage_nummer=int(abfrage_nummer)
    vokabeln=list(abfrage.vokabeln.all())
    liste=abfrage.liste

    if abfrage_nummer<len(vokabeln):
        vokabel = vokabeln[abfrage_nummer]
        #POST
        if request.method=='POST':
            form=EingabeForm(request.POST)
            vokabel.abfragen+=1
            vokabel.percentage=vokabel.korrekt/vokabel.abfragen
            vokabel.save()
            if form.is_valid():
                eingabe=form['eingabe'].value()
                if vokabel.franzoesisch==eingabe:
                    #Weiter zur nächsten Vokabel
                    korrekt=True
                    #Zähle nur als korrekten Versuch, wenn direkt korrekt
                    if erster_versuch=='0':
                        vokabel.korrekt+=1
                        vokabel.percentage = vokabel.korrekt / vokabel.abfragen
                        vokabel.save()
                    #Sonst zähle aber auch Korrekturversuch nicht
                    else:
                        vokabel.abfragen-=1
                        vokabel.save()

                    erster_versuch='0'

                    abfrage_nummer+=1
                    if abfrage_nummer<len(vokabeln):
                        #Neue Vokabel
                        vokabel = vokabeln[abfrage_nummer]
                        form=EingabeForm()
                    else:
                        #Ende der Abfrage
                        context = {'abfrage': abfrage, 'liste': liste}
                        Abfrage.objects.get(id=abfrage.id).delete()
                        return render(request, 'vokabel_trainer/beendete_abfrage.html', context)
                else:
                    erster_versuch='1'
                    korrekt=False
            abfrage_one_up=abfrage_nummer+1
            context = {'abfrage': abfrage, 'abfrage_nummer': abfrage_nummer, 'abfrage_one_up':abfrage_one_up,'form':form, 'vokabel':vokabel,
                       'korrekt':korrekt, 'erster_versuch':erster_versuch}
            return render(request, 'vokabel_trainer/aktive_abfrage.html', context)
        #GET
        else:
            # Wird nur bei der allerersten Vokabelabfrage aufgerufen
            korrekt=True
            form=EingabeForm()
            abfrage_one_up = abfrage_nummer + 1
            context = {'abfrage': abfrage, 'abfrage_nummer': abfrage_nummer, 'abfrage_one_up':abfrage_one_up, 'form': form, 'vokabel':vokabel,
                       'korrekt':korrekt, 'erster_versuch':erster_versuch}
            return render(request, 'vokabel_trainer/aktive_abfrage.html', context)
    else:
        raise Http404