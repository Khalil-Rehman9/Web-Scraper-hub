from django import forms
from .models import FootballMatch
#DataFlair
class UpdateFootballMatch(forms.ModelForm):
    class Meta:
        model = FootballMatch
        fields = '__all__'