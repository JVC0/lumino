from crispy_forms.helper import FormHelper
from django import forms
from crispy_forms.layout import Layout, Field, Submit
from crispy_bootstrap5.bootstrap5 import FloatingField
from .models import Lesson, Subject


class AddLessonForm(forms.ModelForm):
    class Meta:
        model = Lesson
        fields = ('title', 'content')
    
    content = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 6}))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.attrs = {'novalidate': True}  
        self.helper.layout = Layout(
            FloatingField('title'),
            FloatingField('content'),
            Submit('add_lesson', 'Create Lesson', css_class='btn btn-outline-success w-100 mt-2 mb-2'),
        )

class EditLessonForm(forms.ModelForm):
    class Meta:
        model = Lesson
        fields = ('title', 'content')
    
    content = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 6}))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.attrs = {'novalidate': True}  # Desactiva validación HTML5
        self.helper.layout = Layout(
            FloatingField('title'),
            FloatingField('content'),
            Submit('edit_lesson', 'Edit Lesson', css_class='btn btn-outline-warning w-100 mt-2 mb-2'),
        )
class EnrollSubjectsForm(forms.Form):
    subjects = forms.ModelMultipleChoiceField(
        queryset=Subject.objects.all(), widget=forms.CheckboxSelectMultiple
    )

    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['subjects'].queryset = self.fields['subjects'].queryset.exclude(
            pk__in=user.enrolled_subjects.all()
        )
        self.helper = FormHelper()
        self.helper.form_show_labels = False
        self.helper.layout = Layout(
            Field('subjects'), Submit('enroll', 'Enroll', css_class='mt-2 mb2')
        )


class UnenrollSubjectsForm(forms.Form):
    subjects = forms.ModelMultipleChoiceField(
        queryset=Subject.objects.all(), widget=forms.CheckboxSelectMultiple
    )

    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['subjects'].queryset = user.enrolled_subjects.all()
        self.helper = FormHelper()
        self.helper.form_show_labels = False
        self.helper.layout = Layout(
            Field('subjects'), Submit('unenroll', 'Unenroll', css_class='mt-2 mb2')
        )
