from django import forms
from .models import SessionExercise


class SetForm(forms.ModelForm):
    class Meta:
        model = SessionExercise
        exclude = ['session_id', 'exercise_id']
        fields = '__all__'
