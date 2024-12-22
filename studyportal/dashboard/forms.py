from django import forms
from .models import *
from django.contrib.auth.forms import UserCreationForm

class NoteForm(forms.ModelForm):
    class Meta:
        model = Notes
        fields = ['title','description']


class DateInput(forms.DateInput):
    input_type = 'date'


class HomeworkForm(forms.ModelForm):
    class Meta:
        model = Homework
        widgets = {'due': DateInput()}
        fields = ['subject', 'title', 'description',
                 'due', 'status']
        

class DashboardForm(forms.Form):
    text = forms.CharField(max_length=100, label='Enter your seach ')


class TodoForm(forms.ModelForm):
    class Meta:
        model = ToDo
        widgets = {
            'time': forms.TimeInput(attrs={'type': 'time'}),
        }
        fields = ['title', 'time', 'status']


class UserRegistration(UserCreationForm):
    class Meta:
        model = User
        fields = ['username','password1','password2']