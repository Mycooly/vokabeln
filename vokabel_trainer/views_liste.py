from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.db.models.functions import Lower

import numpy as np

from re import compile

from .models import Vokabel, Liste
from .forms import ListeForm, AbfrageForm

# Views in Zusammenhang mit Elementen der Klasse Liste

# Regex zum Einlesen von CSV Vokabellisten
deutsch = r'((?=")"(?P<deutsch1>[^"]+)"|(?P<deutsch2>[^,]+))'
franzoesisch = r'((?=")"(?P<franz1>[^"]+)"|(?P<franz2>[^,]+))'
regex = compile(r'^' + deutsch + r',' + franzoesisch + r'$')


def listen(request):
    """Auflistung aller Vokabellisten"""
    listen = Liste.objects.order_by('name')
    context = {'listen': listen}

    return render(request, 'vokabel_trainer/listen.html', context)


def liste(request, liste_id):
    """Darstellung einer Vokabelliste"""
    liste = Liste.objects.get(id=liste_id)
    vokabeln = liste.vokabel_set.order_by(Lower('deutsch'))
    form = AbfrageForm()

    # Berechne Statistik Parameter
    if vokabeln:
        percent_l, versuche_l = np.array([[vokabel.percentage, vokabel.abfragen] for vokabel in vokabeln]).transpose()
        versuche = round(np.mean(versuche_l), 2)
        if np.sum(versuche_l) > 0:
            erfolgsquote = np.mean(percent_l[versuche_l != 0])
        else:
            erfolgsquote = 0
    else:
        erfolgsquote = 0
        versuche = 0
    context = {'liste': liste, 'vokabeln': vokabeln, 'anzahl_vokabeln': len(vokabeln),
               'erfolgsquote': erfolgsquote, 'versuche': versuche, 'form': form}

    return render(request, 'vokabel_trainer/liste.html', context)


def vokabeln_aus_csv_eintragen(liste, form):
    """Trägt Vokabeln aus CSV in eine Liste ein"""
    liste.file = form['file'].value()
    liste.save()

    # Lese Datei und füge Vokabeln hinzu
    liste.file.open('r')
    line = liste.file.readline()
    while line:
        daten = regex.match(line).groupdict()
        if daten['deutsch1'] and daten['franz1']:
            Vokabel.objects.create(
                liste=liste,
                deutsch=daten['deutsch1'].strip(),
                franzoesisch=daten['franz1'].strip(),
            )
        elif daten['deutsch1'] and daten['franz2']:
            Vokabel.objects.create(
                liste=liste,
                deutsch=daten['deutsch1'].strip(),
                franzoesisch=daten['franz2'].strip(),
            )
        elif daten['deutsch2'] and daten['franz1']:
            Vokabel.objects.create(
                liste=liste,
                deutsch=daten['deutsch2'].strip(),
                franzoesisch=daten['franz1'].strip(),
            )
        else:
            Vokabel.objects.create(
                liste=liste,
                deutsch=daten['deutsch2'].strip(),
                franzoesisch=daten['franz2'].strip(),
            )
        line = liste.file.readline()
    liste.save()
    liste.file.delete()


def neue_liste(request):
    """Erstellt eine neue Vokabelliste"""
    if request.method != 'POST':
        form = ListeForm()
    else:
        form = ListeForm(request.POST, request.FILES or None)
        if form.is_valid():
            liste = Liste.objects.create()
            liste.name = form['name'].value()
            liste.beschreibung = form['beschreibung'].value()
            liste.save()
            if form['file'].value() is not None:
                vokabeln_aus_csv_eintragen(liste, form)

            return HttpResponseRedirect(reverse('vokabel_trainer:liste', args=[liste.id]))
    context = {'form': form}

    return render(request, 'vokabel_trainer/neue_liste.html', context)


def liste_bearbeiten(request, liste_id):
    """Bearbeitet eine Liste"""
    liste = Liste.objects.get(id=liste_id)
    vokabeln = liste.vokabel_set.order_by(Lower('deutsch'))

    if request.method != 'POST':
        form = ListeForm()
        form['name'].initial = liste.name
        form['beschreibung'].initial = liste.beschreibung
    else:
        form = ListeForm(request.POST, request.FILES or None)
        if form.is_valid():
            liste.name = form['name'].value()
            liste.beschreibung = form['beschreibung'].value()
            liste.save()
            if form['file'].value() is not None:
                vokabeln_aus_csv_eintragen(liste, form)

            return HttpResponseRedirect(reverse('vokabel_trainer:liste_bearbeiten', args=[liste.id]))
    context = {'liste': liste, 'vokabeln': vokabeln, 'anzahl_vokabeln': len(vokabeln), 'form': form}

    return render(request, 'vokabel_trainer/liste_bearbeiten.html', context)


def liste_loeschen(request, liste_id):
    """Loescht eine Liste"""
    Liste.objects.get(id=liste_id).delete()

    return HttpResponseRedirect(reverse('vokabel_trainer:listen'))