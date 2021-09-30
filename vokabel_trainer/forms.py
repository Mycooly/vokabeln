from django import forms

from .models import Vokabel


class ListeForm(forms.Form):
    name = forms.CharField(max_length=500, widget=forms.Textarea(attrs={'cols': 80, 'rows': 1, 'autofocus': True}))
    beschreibung = forms.CharField(max_length=2000, required=False,
                                   widget=forms.Textarea(attrs={'cols': 80, 'rows': 4}))
    file = forms.FileField(required=False)


class VokabelForm(forms.ModelForm):
    class Meta:
        model = Vokabel
        fields = ['deutsch', 'franzoesisch']
        labels = {'deutsch': '', 'franzoesisch': ''}
        widgets = {'deutsch': forms.Textarea(attrs={'cols': 80, 'rows': 4, 'autofocus': True}),
                   'franzoesisch': forms.Textarea(attrs={'cols': 80, 'rows': 4})}


class AbfrageForm(forms.Form):
    vokabelzahl = forms.ChoiceField(
        choices=(
            (5, 5),
            (10, 10),
            (20, 20),
        )
    )
    wiederholungen = forms.ChoiceField(
        choices=(
            (1, 1),
            (2, 2),
            (3, 3),
        )
    )


class EingabeForm(forms.Form):
    eingabe = forms.CharField(label='', max_length=1000, required=False ,widget=forms.TextInput(attrs={'size': 100, 'autofocus': True}))
