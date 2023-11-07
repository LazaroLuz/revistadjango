from django import forms
from .models import Comic, Revista


class ComicForm(forms.ModelForm):
    class Meta:
        model = Comic
        fields = ['name', 'description', 'picture']


class RevistaForm(forms.ModelForm):
    file = forms.FileField(
        widget=forms.ClearableFileInput(attrs={"multiple": True})
    )

    class Meta:
        model = Revista
        fields = ['base', 'file']


class FileFieldForm(forms.Form):
    url = forms.URLField()


