from django import forms
from .models import Transaction, Category, Subcategory, Type
import django_filters 
from django.db import models
from .utils import OptionalChoiceField
from django.forms import ModelForm, Textarea
from .widgets import BootstrapDateTimePickerInput

class DynamicChoiceMixin(object):

    @property
    def field(self):
        queryset = self.parent.queryset
        field = super(DynamicChoiceMixin, self).field

        choices = list()
        have = list()
        # iterate through the queryset and pull out the values for the field name
        for item in queryset:
            name = getattr(item, self.field_name)
            if name in have:
                continue
            have.append(name)
            choices.append((name, name))
        field.choices.choices = choices
        return field


class DynamicChoiceFilter(DynamicChoiceMixin, django_filters.ChoiceFilter):
    pass
	
class TransactionsFilter(django_filters.FilterSet):
    amount = django_filters.NumberFilter()
    amount__gt = django_filters.NumberFilter(field_name='amount', lookup_expr='gt')
    amount__lt = django_filters.NumberFilter(field_name='amount', lookup_expr='lt')
	
    transaction_year = django_filters.NumberFilter(field_name='date', lookup_expr='year')
    transaction_year__gt = django_filters.NumberFilter(field_name='date', lookup_expr='year__gt')
    transaction_year__lt = django_filters.NumberFilter(field_name='date', lookup_expr='year__lt')
	
    class Meta:
            model = Transaction
            fields =  ['type','category','subcategory','date','amount__gt','name','transaction_year','transaction_year__gt','transaction_year__lt','description']
            filter_overrides = {
					 models.CharField: {
                 'filter_class': django_filters.CharFilter,
                 'extra': lambda f: {
                     'lookup_expr': 'icontains',
                 },
             },
			}