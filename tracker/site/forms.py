"""This file contains all the project/ticket related forms.

author: Potato
version: 1.0.0

change: SP 2015-11-11 - Change assignee queryset
        SP 2015-11-11 - Adjust assignee widget for easier selection of assignees
"""
from django import forms
from django.contrib.auth import get_user_model

from crispy_forms_foundation.forms import FoundationModelForm

from .models import Project, Ticket


class BaseTrackerForm(FoundationModelForm):
    def __init__(self, user=None, title=None, *args, **kwargs):
        self.title = title
        self.user = user

        super(BaseTrackerForm, self).__init__(*args, **kwargs)

        for field in self.fields.values():
            field.widget.attrs['placeholder'] = field.label

    def save(self, *args, **kwargs):
        commit = kwargs.pop('commit', True)
        instance = super(BaseTrackerForm, self).save(
            commit=False, *args, **kwargs)

        self.pre_save(instance)

        if commit:
            instance.save()

        return instance

    def pre_save(self, instance):
        pass


class ProjectForm(BaseTrackerForm):
    class Meta:
        model = Project
        fields = ('title',)

    def pre_save(self, instance):
        instance.created_by = self.user


class TicketForm(BaseTrackerForm):
    """Ticket form

    change: SP 2015-11-11 - Adjust widgets on assignees field for easier management of assignees
    """
    assignees = forms.ModelMultipleChoiceField(widget=forms.CheckboxSelectMultiple, queryset=None, required=False)

    class Meta:
        model = Ticket
        fields = ('title', 'description', 'assignees',)

    def __init__(self, project=None, *args, **kwargs):
        """Sets additional initial values for the TicketForm

        change: SP 2015-11-11 - Slight queryset adjustment to try to only show email addresses
        """
        self.project = project
        super(TicketForm, self).__init__(*args, **kwargs)

        self.fields['assignees'].queryset = get_user_model().objects.all().only('email')

    def pre_save(self, instance):
        instance.created_by = self.user
        instance.project = self.project
