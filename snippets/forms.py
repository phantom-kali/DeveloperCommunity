from django import forms
from .models import CodeSnippet

class CodeSnippetForm(forms.ModelForm):
    class Meta:
        model = CodeSnippet
        fields = ['title', 'code', 'language', 'description']