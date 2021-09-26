from django.shortcuts import render
from django.http import HttpResponseRedirect, Http404
from django.urls import reverse
from django.db.models.functions import Lower
from numpy.random import choice
from numpy.random import shuffle
from numpy import sum
from math import cos
from datetime import datetime
from re import findall
import re

from .models import Liste, Abfrage, Vokabel
from .forms import ListeForm, VokabelForm, AbfrageForm, EingabeForm

# Create your views here.
regex=re.compile(r'^((?=")"(?P<deutsch1>[^"]+)"|(?P<deutsch2>[^,]+)),((?=")"(?P<franz1>[^"]+)"|(?P<franz2>[^,]+))')

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
    vokabeln=liste.vokabel_set.order_by(Lower('deutsch'))
    if vokabeln:
        vokabelzahl=len(vokabeln)
        statistik=[[vokabel.percentage,vokabel.korrekt,vokabel.abfragen] for vokabel in vokabeln]
        erfolgsquote,_,versuche=sum(statistik,axis=0)
        versuche=round(versuche/vokabelzahl,2)
        erfolgsquote=erfolgsquote/vokabelzahl
    else:
        erfolgsquote=0
        versuche=0
    context={'liste':liste, 'vokabeln':vokabeln, 'anzahl_vokabeln':len(vokabeln),
             'form':form,'erfolgsquote':erfolgsquote,'versuche':versuche}
    return render(request, 'vokabel_trainer/liste.html', context)

def neue_liste(request):
    """Erstellt neue Vokabelliste"""
    form=ListeForm()
    if request.method =='POST':
        form=ListeForm(request.POST, request.FILES or None)
        if form.is_valid():
            liste=Liste.objects.create()
            liste.beschreibung=form['beschreibung'].value()
            if form['file']:
                liste.file=form['file'].value()
                liste.save()

                #File reading
                liste.file.open('r')
                line=liste.file.readline()
                while line:
                    daten=regex.match(line).groupdict()
                    if daten['deutsch1'] and daten['franz1']:
                        neue_vokabel = Vokabel.objects.create(
                            liste=liste,
                            deutsch=daten['deutsch1'].strip(),
                            franzoesisch=daten['franz1'].strip(),
                        )
                    elif daten['deutsch1'] and daten['franz2']:
                        neue_vokabel = Vokabel.objects.create(
                            liste=liste,
                            deutsch=daten['deutsch1'].strip(),
                            franzoesisch=daten['franz2'].strip(),
                        )
                    elif daten['deutsch2'] and daten['franz1']:
                        neue_vokabel = Vokabel.objects.create(
                            liste=liste,
                            deutsch=daten['deutsch2'].strip(),
                            franzoesisch=daten['franz1'].strip(),
                        )
                    else:
                        neue_vokabel = Vokabel.objects.create(
                            liste=liste,
                            deutsch=daten['deutsch2'].strip(),
                            franzoesisch=daten['franz2'].strip(),
                        )
                    line=liste.file.readline()

                liste.file.delete()

            return HttpResponseRedirect(reverse('vokabel_trainer:liste',args=[liste.id]))

    context ={'form':form}
    return render(request, 'vokabel_trainer/neue_liste.html', context)

def liste_bearbeiten(request,liste_id):
    """Bearbeitet Liste"""
    liste=Liste.objects.get(id=liste_id)
    vokabeln=liste.vokabel_set.order_by(Lower('deutsch'))

    context={'liste':liste, 'vokabeln':vokabeln, 'anzahl_vokabeln':len(vokabeln)}
    return render(request, 'vokabel_trainer/liste_bearbeiten.html', context)

def neue_vokabel(request,liste_id):
    """Erstellt neue Vokabel"""
    liste=Liste.objects.get(id=liste_id)
    vokabeln=liste.vokabel_set.order_by(Lower('deutsch'))

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

def vokabel_bearbeiten(request, vokabel_id):
    """Bearbeitet Vokabel"""
    vokabel=Vokabel.objects.get(id=vokabel_id)
    liste=vokabel.liste
    if request.method == 'POST':
        form=VokabelForm(data=request.POST)
        if form.is_valid:
            vokabel.deutsch=form['deutsch'].value().strip()
            vokabel.franzoesisch=form['franzoesisch'].value().strip()
            vokabel.save()
            return HttpResponseRedirect(reverse('vokabel_trainer:liste_bearbeiten',args=[liste.id]))
    else:
        form=VokabelForm(instance=vokabel)
        context={'vokabel':vokabel, 'vokabel_id':vokabel.id, 'form':form, 'liste':liste}
        return render(request, 'vokabel_trainer/vokabel_bearbeiten.html', context)

def abfrage(request,abfrage_id):
    """Zeigt Abfrage"""
    abfrage=Abfrage.objects.get(id=abfrage_id)
    liste=abfrage.liste
    vokabeln=abfrage.vokabeln.order_by(Lower('deutsch'))

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

        wiederholungen=int(form['wiederholungen'].value())
        reihenfolge=wiederholungen*list(range(vokabelzahl))
        shuffle(reihenfolge)
        reihenfolge=' '.join(map(str,reihenfolge))

        neue_abfrage=Abfrage.objects.create(
            liste=liste,
            date_added=datetime.now(),
            reihenfolge=reihenfolge,
        )
        neue_abfrage.vokabeln.set(vokabeln)
        return HttpResponseRedirect(reverse('vokabel_trainer:abfrage',args=[neue_abfrage.id]))

def aktive_abfrage(request, abfrage_id, abfrage_nummer, erster_versuch, anzahl_versuche):
    """Führt eine Abfrage durch"""
    abfrage=Abfrage.objects.get(id=abfrage_id)
    abfrage_nummer=int(abfrage_nummer)
    vokabeln=list(abfrage.vokabeln.all())
    liste=abfrage.liste
    anzahl_versuche = int(anzahl_versuche) + 1

    reihenfolge=abfrage.reihenfolge
    reihenfolge=findall(r'\d+\b',reihenfolge)

    if abfrage_nummer<len(reihenfolge):
        objekt = int(reihenfolge[abfrage_nummer])
        vokabel = vokabeln[objekt]
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
                        #Cheaten
                        if 'korrektur' in request.POST:
                            vokabel.korrekt += 1
                        vokabel.abfragen-=1
                        vokabel.percentage = vokabel.korrekt / vokabel.abfragen
                        vokabel.save()

                    erster_versuch='0'

                    abfrage_nummer+=1
                    if abfrage_nummer<len(reihenfolge):
                        #Neue Vokabel

                        objekt = int(reihenfolge[abfrage_nummer])
                        vokabel = vokabeln[objekt]
                        form=EingabeForm()
                    else:
                        #Ende der Abfrage
                        anzahl_versuche-=1
                        erfolgsquote=len(reihenfolge)/anzahl_versuche
                        context = {'liste': liste,'vokabelzahl':len(vokabeln),'anzahl_versuche':anzahl_versuche,'erfolgsquote':erfolgsquote}
                        Abfrage.objects.get(id=abfrage.id).delete()
                        return render(request, 'vokabel_trainer/beendete_abfrage.html', context)
                else:
                    erster_versuch='1'
                    korrekt=False
            abfrage_one_up=abfrage_nummer+1
            context = {'abfrage': abfrage, 'abfrage_nummer': abfrage_nummer, 'abfrage_one_up':abfrage_one_up,'form':form, 'vokabel':vokabel,
                       'korrekt':korrekt, 'erster_versuch':erster_versuch, 'anzahl_versuche':anzahl_versuche,
                       'objekt':objekt, 'reihenfolge':reihenfolge}
            return render(request, 'vokabel_trainer/aktive_abfrage.html', context)
        #GET
        else:
            # Wird nur bei der allerersten Vokabelabfrage aufgerufen
            korrekt=True
            form=EingabeForm()
            objekt = int(reihenfolge[0])
            abfrage_one_up = abfrage_nummer + 1
            context = {'abfrage': abfrage, 'abfrage_nummer': abfrage_nummer, 'abfrage_one_up':abfrage_one_up, 'form': form, 'vokabel':vokabel,
                       'korrekt':korrekt, 'erster_versuch':erster_versuch,'anzahl_versuche':anzahl_versuche,
                       'objekt':objekt, 'reihenfolge':reihenfolge}
            return render(request, 'vokabel_trainer/aktive_abfrage.html', context)
    else:
        raise Http404

def abfrage_abbrechen(request, abfrage_id):
    liste=Abfrage.objects.get(id=abfrage_id).liste
    Abfrage.objects.get(id=abfrage_id).delete()
    return HttpResponseRedirect(reverse('vokabel_trainer:liste',args=[liste.id]))
