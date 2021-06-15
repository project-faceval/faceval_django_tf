from django import forms


class PredicatedCandidateForm(forms.Form):
    ext = forms.CharField()
    bimg = forms.ImageField()
    pos_set = forms.CharField()


class PredicatedCandidateFormBase64(forms.Form):
    ext = forms.CharField()
    bimg = forms.CharField()
    pos_set = forms.CharField()
