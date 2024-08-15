from django import forms
from .models import ErrorMessage, Solution

class ErrorMessageForm(forms.ModelForm):
    class Meta:
        model = ErrorMessage
        fields = ['title', 'error_message', 'steps_to_reproduce', 'expected_behavior', 'actual_behavior']

class SolutionForm(forms.ModelForm):
    class Meta:
        model = Solution
        fields = ['content']