from django import forms
from .models import Consultation
import django_filters 

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


class ConsultationFilter(django_filters.FilterSet):
	specialism = DynamicChoiceFilter(field_name='specialism')
	location = DynamicChoiceFilter(field_name='location')
	upsurge = DynamicChoiceFilter(field_name='upsurge')

	class Meta:
			model = Consultation
			fields =  ['doctor','specialism','location','upsurge']
