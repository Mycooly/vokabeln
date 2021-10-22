from django import forms

from .models import Vokabel


class ListeForm(forms.Form):
    name = forms.CharField(max_length=500, widget=forms.Textarea(attrs={
        'cols': 80, 'rows': 1, 'autofocus': True, 'autocomplete': 'off'}))
    beschreibung = forms.CharField(max_length=2000, required=False,
                                   widget=forms.Textarea(attrs={'cols': 80, 'rows': 4, 'autocomplete': 'off'}))
    file = forms.FileField(required=False)


class VokabelForm(forms.ModelForm):
    deutsch = forms.CharField(
        max_length=255,
        widget=forms.TextInput(attrs={'autofocus': True, 'autocomplete': 'off', 'size': '81'})
    )
    franzoesisch = forms.CharField(
        max_length=255,
        widget=forms.TextInput(attrs={'autocomplete': 'off', 'size': '81'})
    )

    # forms.Textarea(attrs={'cols': 80, 'rows': 1, 'autofocus': True})
    # forms.Textarea(attrs={'cols': 80, 'rows': 1, 'autocomplete': 'off'})
    widgets = {'deutsch': '',
               'franzoesisch': ''}

    class Meta:
        model = Vokabel
        fields = ['deutsch', 'franzoesisch']
        labels = {'deutsch': '', 'franzoesisch': ''}


class AbfrageForm(forms.Form):
    vokabelzahl = forms.ChoiceField(
        choices=(
            (10, 10),
            (20, 20),
            (30, 30),
        ), initial=30
    )
    wiederholungen = forms.ChoiceField(
        choices=(
            (1, 1),
            (2, 2),
            (3, 3),
        ), initial=3
    )


class EingabeForm(forms.Form):
    eingabe = forms.CharField(label='', max_length=1000, required=False,
                              widget=forms.TextInput(
                                  attrs={'size': 50, 'autofocus': True, 'autocomplete': 'off', 'class': 'text-center'}))
