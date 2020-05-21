from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
from taggit.forms import TagField
from taggit_labels.widgets import LabelWidget

from blog.models import Post, Meet
from users.models import User


def f(v):
    a = 2
    raise ValidationError()


class MeetForm(forms.ModelForm):
    title = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Title'}))
    # text = forms.CharField(
    #     label='Text',
    # widget=forms.Textarea(attrs={'placeholder': 'Text'})
    # )

    meet_date = forms.DateTimeField(input_formats=['%Y-%m-%dT%H:%M'],
                                    widget=forms.DateTimeInput(attrs={'type': 'datetime-local'}),
                                    help_text=_("Speсify thr date and time of the meet"),
                                    validators=[])

    tags = TagField(required=False, widget=LabelWidget)

    lat = forms.FloatField(
        widget=forms.HiddenInput()
    )
    lng = forms.FloatField(
        widget=forms.HiddenInput()
    )

    class Meta:
        model = Meet
        fields = ['meet_date', 'lat', 'lng', 'title', 'tags']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_show_labels = True
        self.helper.layout = Layout(
            Row(
                Column('meet_date', css_class='form-group col-md-3 mb-0'),
                Column('title', css_class='form-group col-md-9 mb-0'),
                # Column('main_img', css_class='form-group col-md-6 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column('lat', css_class='form-group col-md-3 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column('lng', css_class='form-group col-md-3 mb-0'),
                css_class='form-row'
            ),
            'tags',
            Submit('submit', 'Create')
        )


class PostForm(forms.ModelForm):
    title = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Title'}))
    text = forms.CharField(
        # label='Text',
        widget=forms.Textarea(attrs={'placeholder': 'Text'})
    )
    main_img = forms.FileField(required=False)

    author = forms.ModelChoiceField(queryset=User.objects.all(), widget=forms.HiddenInput())

    tags = TagField(required=False, widget=LabelWidget)

    class Meta:
        model = Post
        fields = ['title', 'text', 'main_img', 'author', 'tags']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_show_labels = True
        self.helper.layout = Layout(
            Row(
                Column('title', css_class='form-group col-md-6 mb-0'),
                Column('main_img', css_class='form-group col-md-6 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column('text', css_class='form-group col-md-12 mb-0'),
                css_class='form-row'
            ),
            'author',
            'tags',
            Submit('submit', 'Create')
        )
