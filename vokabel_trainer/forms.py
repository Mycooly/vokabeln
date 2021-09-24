from django import forms

from.models import Liste, Vokabel, Abfrage

class ListeForm(forms.ModelForm):
    class Meta:
        model=Liste
        fields=['beschreibung']
        labels={'beschreibung':''}

class VokabelForm(forms.ModelForm):
    class Meta:
        model=Vokabel
        fields=['deutsch','franzoesisch']
        labels={'deutsch':'','franzoesisch':''}

class AbfrageForm(forms.ModelForm):
    class Meta:
        model=Abfrage
        fields=[]
        labels={}

class EingabeForm(forms.Form):
    eingabe=forms.CharField(label='eingabe', max_length=200)