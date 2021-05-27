from django import forms


class PredicatedCandidateForm(forms.Form):
    ext = forms.CharField()
    bimg = forms.ImageField()
    pos_set = forms.CharField()
