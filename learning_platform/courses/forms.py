from django import forms
from .models import Course, Lesson
class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ['title', 'description']

class LessonForm(forms.ModelForm):
    class Meta:
        model = Lesson
        fields = ['title', 'content', 'order', 'video']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'content': forms.Textarea(attrs={'class': 'form-control'}),
            'video': forms.FileInput(attrs={'class': 'form-control'}),
        }
