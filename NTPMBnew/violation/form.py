from django import forms


class ChercheForm(forms.Form):
    recherchetexte = forms.CharField(label='Type ONLY the begining of the Criminal Code number: type 140 to find VIOLATION for 140.2(a)', max_length=100)