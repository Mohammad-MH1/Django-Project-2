
from django import forms
from django.db import models
from django.db.models import fields
from django.forms import ModelForm
from django import forms
from .models import Project, Review


class ProjectForm(ModelForm):
    class Meta:
        model = Project
        fields = ['title', 'featured_image', 'description',
                  'source_link', ]
        widgets = {
            'tags': forms.CheckboxSelectMultiple(),
        }

    def __init__(self, *args, **kwargs):
        super(ProjectForm, self).__init__(*args, **kwargs)

        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'input'})

        # self.fields['title'].widget.attrs.update(
        #     {'class': 'input', 'placeholder': 'Add Title'})


class ReviewForm(ModelForm):
    class Meta:
        model = Review
        fields = ['value', 'body']

        labels = {
            'value': 'Place your Vote',
            'body': 'Add a comment with your Vote'
        }

    def __init__(self, *args, **kwargs):
        super(ReviewForm, self).__init__(*args, **kwargs)

        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'input'})
