import datetime

from django import forms
from oscar.forms import widgets
from django.utils import six
from django.utils.translation import ugettext_lazy as _
from django.core.validators import MinValueValidator
from oscar.core.loading import get_model

ConditionalOffer = get_model('offer', 'ConditionalOffer')
Condition = get_model('offer', 'Condition')
Benefit = get_model('offer', 'Benefit')


class RestrictionsForm(forms.ModelForm):

    start_datetime = forms.DateTimeField(
        widget=widgets.DateTimePickerInput(),
        label=_("Start date"), required=False)
    end_datetime = forms.DateTimeField(
        widget=widgets.DateTimePickerInput(),
        label=_("End date"), required=False)
    # Some complicated situations require offers to be applied in a set order.
    priority = forms.IntegerField(
        label=_("Priority"), validators=[MinValueValidator(1)], initial=1,
        help_text=_("The highest priority offers are applied first"))

    def __init__(self, *args, **kwargs):
        super(RestrictionsForm, self).__init__(*args, **kwargs)
        today = datetime.date.today()
        self.fields['start_datetime'].initial = today

    class Meta:
        model = ConditionalOffer
        fields = ('start_datetime', 'end_datetime',
                  'priority', 'exclusive')

    def clean(self):
        cleaned_data = super(RestrictionsForm, self).clean()
        start = cleaned_data['start_datetime']
        end = cleaned_data['end_datetime']
        if start and end and end < start:
            raise forms.ValidationError(_(
                "The end date must be after the start date"))
        return cleaned_data


class ConditionForm(forms.ModelForm):
    COUNT, VALUE, COVERAGE = ("Count", "Value", "Coverage")

    TYPE_CHOICES = (
        (COUNT, _("Depends on number of items in basket that are in "
                  "condition range")))

    custom_condition = forms.ChoiceField(
        required=False,
        label=_("Custom condition"), choices=())
    # type = forms.ChoiceField(label=_('Type'), choices=TYPE_CHOICES)

    def __init__(self, *args, **kwargs):
        super(ConditionForm, self).__init__(*args, **kwargs)

        custom_conditions = Condition.objects.all().exclude(
            proxy_class=None)
        if len(custom_conditions) > 0:
            # Initialise custom_condition field
            choices = [(c.id, six.text_type(c)) for c in custom_conditions]
            choices.insert(0, ('', ' --------- '))
            self.fields['custom_condition'].choices = choices
            condition = kwargs.get('instance')
            if condition:
                self.fields['custom_condition'].initial = condition.id
        else:
            # No custom conditions and so the type/range/value fields
            # are no longer optional
            for field in ('type', 'range', 'value'):
                self.fields[field].required = True
                if field == 'type':
                    self.fields[field].choices = [f for f in self.fields[field].choices
                                                  if f[0] not in ['Value', 'Coverage']]

    class Meta:
        model = Condition
        fields = ['range', 'type', 'value']

    def clean(self):
        data = super(ConditionForm, self).clean()

        # Check that either a condition has been entered or a custom condition
        # has been chosen
        if not any(data.values()):
            raise forms.ValidationError(
                _("Please either choose a range, type and value OR "
                  "select a custom condition"))

        if not data['custom_condition']:
            if not data.get('range', None):
                raise forms.ValidationError(
                    _("A range is required"))

        return data

    def save(self, *args, **kwargs):
        # We don't save a new model if a custom condition has been chosen,
        # we simply return the instance that has been chosen
        if self.cleaned_data['custom_condition']:
            return Condition.objects.get(
                id=self.cleaned_data['custom_condition'])
        return super(ConditionForm, self).save(*args, **kwargs)


class BenefitForm(forms.ModelForm):
    custom_benefit = forms.ChoiceField(
        required=False,
        label=_("Custom incentive"), choices=())

    def __init__(self, *args, **kwargs):
        super(BenefitForm, self).__init__(*args, **kwargs)

        custom_benefits = Benefit.objects.all().exclude(
            proxy_class=None)
        if len(custom_benefits) > 0:
            # Initialise custom_benefit field
            choices = [(c.id, six.text_type(c)) for c in custom_benefits]
            choices.insert(0, ('', ' --------- '))
            self.fields['custom_benefit'].choices = choices
            benefit = kwargs.get('instance')
            if benefit:
                self.fields['custom_benefit'].initial = benefit.id
        else:
            # No custom benefit and so the type fields
            # are no longer optional
            self.fields['type'].required = True

    class Meta:
        model = Benefit
        fields = ['range', 'type', 'value']

    def clean(self):
        data = super(BenefitForm, self).clean()

        # Check that either a benefit has been entered or a custom benfit
        # has been chosen
        if not any(data.values()):
            raise forms.ValidationError(
                _("Please either choose a range, type and value OR "
                  "select a custom incentive"))

        if data['custom_benefit'] and (data.get('range') or data.get('type') or data.get('value')):
            raise forms.ValidationError(
                _("No other options can be set if you are using a "
                  "custom incentive"))

        return data

    def save(self, *args, **kwargs):
        # We don't save a new model if a custom benefit has been chosen,
        # we simply return the instance that has been chosen
        if self.cleaned_data['custom_benefit']:
            return Benefit.objects.get(
                id=self.cleaned_data['custom_benefit'])
        return super(BenefitForm, self).save(*args, **kwargs)
