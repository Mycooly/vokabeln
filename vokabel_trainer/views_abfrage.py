from django.shortcuts import render
from django.http import HttpResponseRedirect, Http404, JsonResponse
from django.urls import reverse
from django.db.models.functions import Lower

from numpy.random import choice, shuffle
from numpy import sum

from math import cos

from datetime import datetime

from re import findall

from .models import Liste, Abfrage
from .forms import EingabeForm, AbfrageForm


# Views in Zusammenhang mit Elementen der Klasse Abfrage

def abfrage(request, abfrage_id):
    """Zeigt eine Abfrage an"""
    abfrage = Abfrage.objects.get(id=abfrage_id)
    liste = abfrage.liste
    vokabeln = abfrage.vokabeln.order_by(Lower('deutsch'))

    context = {'abfrage': abfrage, 'liste': liste, 'vokabeln': vokabeln}
    return render(request, 'vokabel_trainer/abfrage.html', context)


def neue_abfrage(request, liste_id):
    """Erstellt eine neue Abfrage"""
    if request.method != 'POST':
        raise Http404
    else:
        liste = Liste.objects.get(id=liste_id)
        vokabeln = list(liste.vokabel_set.all())
        form = AbfrageForm(request.POST)

        # Wähle zufällig Vokabeln gewichtet nach Erfolgsquote aus
        weights = [cos(vokabel.percentage) for vokabel in vokabeln]
        weights = weights / sum(weights)
        vokabelzahl = int(form['vokabelzahl'].value())
        vokabeln = choice(vokabeln, size=min(vokabelzahl, len(vokabeln)), replace=False, p=weights)

        # Erstelle zufällige Liste, in welcher Reihenfolge diese Vokabeln wie oft
        # abgefragt werden sollen
        wiederholungen = int(form['wiederholungen'].value())
        reihenfolge = wiederholungen * list(range(vokabelzahl))
        shuffle(reihenfolge)
        reihenfolge = ' '.join(map(str, reihenfolge))

        neue_abfrage = Abfrage.objects.create(
            liste=liste,
            date_added=datetime.now(),
            reihenfolge=reihenfolge,
            anzahl_abfragen=wiederholungen*vokabelzahl,
            wiederholungen=wiederholungen,
        )
        neue_abfrage.vokabeln.set(vokabeln)

        return HttpResponseRedirect(reverse('vokabel_trainer:abfrage', args=[neue_abfrage.id]))


def aktive_abfrage(request, abfrage_id, abfrage_nummer, erster_versuch, anzahl_versuche, tipp_nr):
    """Führt eine Abfrage durch"""
    abfrage = Abfrage.objects.get(id=abfrage_id)
    abfrage_nummer = int(abfrage_nummer)
    vokabeln = list(abfrage.vokabeln.all())
    liste = abfrage.liste
    anzahl_versuche = int(anzahl_versuche) + 1
    reihenfolge = findall(r'\d+\b', abfrage.reihenfolge)

    if abfrage_nummer < len(reihenfolge):
        vokabel_index = int(reihenfolge[abfrage_nummer])
        vokabel = vokabeln[vokabel_index]
        korrekt = False

        # POST
        if request.method == 'POST':
            form = EingabeForm(request.POST)
            vokabel.abfragen += 1
            vokabel.percentage = vokabel.korrekt / vokabel.abfragen
            vokabel.save()

            if form.is_valid():
                eingabe = form['eingabe'].value()

                # Korrekte Eingabe
                if vokabel.franzoesisch == eingabe:
                    tipp_nr = 0
                    korrekt = True
                    # Zähle Versuch nur, wenn direkt korrekt
                    if erster_versuch == '0':
                        vokabel.korrekt += 1
                        vokabel.stufe += 1
                        vokabel.percentage = vokabel.korrekt / vokabel.abfragen
                        vokabel.save()
                    # Sonst zähle Korrekturversuch nicht
                    else:
                        # Cheaten bei Vertippen
                        if 'korrektur' in request.POST:
                            vokabel.korrekt += 1
                            vokabel.stufe += 1
                            anzahl_versuche -= 1
                        # Zähle Korrekturversuch nicht
                        vokabel.abfragen -= 1
                        vokabel.percentage = vokabel.korrekt / vokabel.abfragen
                        vokabel.save()

                    # Nächste Vokabel, also neuer Versuch
                    erster_versuch = '0'
                    abfrage_nummer += 1

                    if abfrage_nummer < len(reihenfolge):
                        # Neue Vokabel
                        vokabel_index = int(reihenfolge[abfrage_nummer])
                        vokabel = vokabeln[vokabel_index]
                        form = EingabeForm()
                    else:
                        # Ende der Abfrage
                        anzahl_versuche -= 1
                        erfolgsquote = len(reihenfolge) / anzahl_versuche
                        context = {'liste': liste, 'vokabelzahl': len(vokabeln), 'anzahl_versuche': anzahl_versuche,
                                   'erfolgsquote': erfolgsquote}
                        for vokabel in vokabeln:
                            vokabel.stufe=0
                            vokabel.save()
                        Abfrage.objects.get(id=abfrage.id).delete()

                        return render(request, 'vokabel_trainer/beendete_abfrage.html', context)

                # Falsche Eingabe
                else:
                    # Zeigt nächsten korrekten Buchstaben und zählt Eingabe nicht
                    if 'tipp' in request.POST:
                        tipp_nr = int(tipp_nr)
                        tipp_nr += 1
                        vokabel.abfragen -= 1
                        vokabel.save()
                        anzahl_versuche -= 1
                        erster_versuch = '0'
                        korrekt = True
                        tipp = vokabel.franzoesisch[:tipp_nr]
                        form = EingabeForm({'eingabe': tipp})
                    else:
                        erster_versuch = '1'
                        korrekt = False

            abfrage_one_up = abfrage_nummer + 1
            context = {'abfrage': abfrage, 'abfrage_nummer': abfrage_nummer, 'abfrage_one_up': abfrage_one_up,
                       'anzahl_abfragen': abfrage.anzahl_abfragen, 'form': form, 'vokabel': vokabel,
                       'vokabel_index': vokabel_index, 'reihenfolge': reihenfolge, 'korrekt': korrekt,
                       'erster_versuch': erster_versuch, 'anzahl_versuche': anzahl_versuche, 'tipp_nr': tipp_nr}

            return render(request, 'vokabel_trainer/aktive_abfrage.html', context)

        # GET
        else:
            # Wird nur bei der allerersten Vokabelabfrage aufgerufen
            korrekt = True
            form = EingabeForm()
            vokabel_index = int(reihenfolge[0])
            abfrage_one_up = abfrage_nummer + 1
            context = {'abfrage': abfrage, 'abfrage_nummer': abfrage_nummer, 'abfrage_one_up': abfrage_one_up,
                       'anzahl_abfragen': abfrage.anzahl_abfragen, 'form': form, 'vokabel': vokabel,
                       'vokabel_index': vokabel_index, 'reihenfolge': reihenfolge, 'korrekt': korrekt,
                       'erster_versuch': erster_versuch, 'anzahl_versuche': anzahl_versuche, 'tipp_nr': tipp_nr}

            return render(request, 'vokabel_trainer/aktive_abfrage.html', context)

    # abfrage_nummer out of range
    else:
        raise Http404


def abfrage_abbrechen(request, abfrage_id):
    """Bricht die aktive Abfrage ab"""
    abfrage = Abfrage.objects.get(id=abfrage_id)
    liste = abfrage.liste
    vokabeln = list(abfrage.vokabeln.all())
    for vokabel in vokabeln:
        vokabel.stufe=0
        vokabel.save()

    Abfrage.objects.get(id=abfrage_id).delete()

    return HttpResponseRedirect(reverse('vokabel_trainer:liste', args=[liste.id]))


def population_chart(request, abfrage_id):
    """Malt die aktuellen Stats der Abfrage"""
    abfrage = Abfrage.objects.get(id=abfrage_id)
    vokabeln = list(abfrage.vokabeln.all())
    stufen=[0 for i in range(abfrage.wiederholungen+1)]

    for vokabel in vokabeln:
        stufen[vokabel.stufe]+=1

    labels = ['0x Korrekt','1x Korrekt','2x Korrekt','3x Korrekt']
    labels = labels[:len(stufen)]
    data = stufen

    return JsonResponse(data={
        'labels': labels,
        'data': data,
    })
