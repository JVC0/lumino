from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, Submit, Div
from django import forms
from .models import Profile

class EditProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('avatar', 'bio')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.attrs = {'novalidate': True}  
        self.helper.layout = Layout(
            Div(
                Field('avatar', css_class='form-control mb-3'),
                Field('bio', css_class='form-control mb-3', rows="6"),
                css_class='form-group'
            ),
            Submit('submit', 'Save Changes', css_class='btn btn-primary btn-block mt-4 rounded-pill')
        )
