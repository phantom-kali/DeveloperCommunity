from django import forms
from .models import ErrorMessage, Solution

class ErrorMessageForm(forms.ModelForm):
    class Meta:
        model = ErrorMessage
        fields = ['title', 'error_message', 'steps_to_reproduce', 'expected_behavior', 'actual_behavior']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'error_message': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'steps_to_reproduce': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'expected_behavior': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'actual_behavior': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
        }

class SolutionForm(forms.ModelForm):
    class Meta:
        model = Solution
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
        }