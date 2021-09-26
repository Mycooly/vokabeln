from django import forms

from.models import Liste, Vokabel, Abfrage

class ListeForm(forms.Form):
    beschreibung = forms.CharField(max_length=500)
    file=forms.FileField(required=False)

class VokabelForm(forms.ModelForm):
    class Meta:
        model=Vokabel
        fields=['deutsch','franzoesisch']
        labels={'deutsch':'','franzoesisch':''}

class AbfrageForm(forms.Form):
    vokabelzahl=forms.ChoiceField(
        choices = (
            (5,5),
            (10,10),
            (20,20),
        )
    )
    wiederholungen=forms.ChoiceField(
        choices=(
            (1,1),
            (2,2),
            (3,3),
        )
    )

class EingabeForm(forms.Form):
    eingabe=forms.CharField(label='', max_length=1000, widget=forms.Textarea(attrs={'cols':80,'rows':4}))


