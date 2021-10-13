from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.db.models.functions import Lower

from .models import Liste, Vokabel
from .forms import VokabelForm


# Views in Zusammenhang mit Elementen der Klasse Vokabel

def neue_vokabel(request, liste_id):
    """Erstellt eine neue Vokabel"""
    liste = Liste.objects.get(id=liste_id)
    vokabeln = liste.vokabel_set.order_by(Lower('deutsch'))

    if request.method != 'POST':
        form = VokabelForm()
    else:
        form = VokabelForm(data=request.POST)
        if form.is_valid():
            neue_vokabel = form.save(commit=False)
            neue_vokabel.liste = liste
            neue_vokabel.save()
            return HttpResponseRedirect(reverse('vokabel_trainer:neue_vokabel', args=[liste_id]))

    context = {'liste': liste, 'form': form, 'vokabeln': vokabeln}
    return render(request, 'vokabel_trainer/neue_vokabel.html', context)


def vokabel_bearbeiten(request, vokabel_id):
    """Bearbeitet eine Vokabel"""
    vokabel = Vokabel.objects.get(id=vokabel_id)
    liste = vokabel.liste

    if request.method != 'POST':
        form = VokabelForm(instance=vokabel)
    else:
        form = VokabelForm(data=request.POST)
        if form.is_valid:
            vokabel.deutsch = form['deutsch'].value().strip()
            vokabel.franzoesisch = form['franzoesisch'].value().strip()
            vokabel.save()
            return HttpResponseRedirect(reverse('vokabel_trainer:liste_bearbeiten', args=[liste.id]))

    context = {'vokabel': vokabel, 'form': form, 'liste': liste}
    return render(request, 'vokabel_trainer/vokabel_bearbeiten.html', context)


def vokabel_loeschen(request, vokabel_id):
    """Löscht eine Vokabel"""
    liste = Vokabel.objects.get(id=vokabel_id).liste
    Vokabel.objects.get(id=vokabel_id).delete()

    return HttpResponseRedirect(reverse('vokabel_trainer:liste_bearbeiten', args=[liste.id]))
