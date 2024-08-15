from django import forms
from .models import Document, EducationalLink

class DocumentForm(forms.ModelForm):
    class Meta:
        model = Document
        fields = ['title', 'description', 'file', 'category']

class EducationalLinkForm(forms.ModelForm):
    class Meta:
        model = EducationalLink
        fields = ['title', 'url', 'description', 'category']