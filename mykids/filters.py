from django import forms
from .models import DagboekPost, Video, Image, Rating
import django_filters 
from django.db import models

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

class ImageFilter(django_filters.FilterSet):

	class Meta:
			model = Image
			fields =  ['id','dagboekpost','rating','desc','imglotte','imgmerlijn','imgpapa','imgmama']
			filter_overrides = {
					 models.CharField: {
                 'filter_class': django_filters.CharFilter,
                 'extra': lambda f: {
                     'lookup_expr': 'icontains',
                 },
             },
			}

class DagboekFilter(django_filters.FilterSet):
	# mijlpaal = DynamicChoiceFilter(field_name='mijlpaal')

	class Meta:
			model = DagboekPost
			fields =  ['id','mijlpaal','titel_lotte','titel_merlijn','beschrijving_lotte','beschrijving_merlijn','favpost']
			filter_overrides = {
					 models.CharField: {
                 'filter_class': django_filters.CharFilter,
                 'extra': lambda f: {
                     'lookup_expr': 'icontains',
                 },
             },
			}
			

class VideoFilter(django_filters.FilterSet):
	rating = DynamicChoiceFilter(field_name='rating')

	class Meta:
			model = Video
			fields =  ['id','dagboekpost','rating','desc','vidlotte','vidmerlijn','vidpapa','vidmama']
			filter_overrides = {
					 models.CharField: {
                 'filter_class': django_filters.CharFilter,
                 'extra': lambda f: {
                     'lookup_expr': 'icontains',
                 },
             },
			}