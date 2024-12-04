from crispy_forms.helper import FormHelper
from crispy_forms.layout import Field, Layout, Submit
from django import forms

from .models import Lesson, Subject


class AddLessonForm(forms.ModelForm):
    class Meta:
        model = Lesson
        fields = ('title', 'content')


class EditLessonForm(forms.ModelForm):
    class Meta:
        model = Lesson
        fields = ('title', 'content')


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
