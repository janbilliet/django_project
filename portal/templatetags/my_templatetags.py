from django import template
from django.contrib.humanize.templatetags.humanize import intcomma
register = template.Library()

@register.filter
def sort_by(queryset, order):
    return queryset.order_by(order)

@register.simple_tag(takes_context=True)
def param_replace(context, **kwargs):
    """
    Return encoded URL parameters that are the same as the current
    request's parameters, only with the specified GET parameters added or changed.

    It also removes any empty parameters to keep things neat,
    so you can remove a parm by setting it to ``""``.

    For example, if you're on the page ``/things/?with_frosting=true&page=5``,
    then

    <a href="/things/?{% param_replace page=3 %}">Page 3</a>

    would expand to

    <a href="/things/?with_frosting=true&page=3">Page 3</a>

    Based on
    https://stackoverflow.com/questions/22734695/next-and-before-links-for-a-django-paginated-query/22735278#22735278
    """
    d = context['request'].GET.copy()
    for k, v in kwargs.items():
        d[k] = v
    for k in [k for k, v in d.items() if not v]:
        del d[k]
    return d.urlencode()
	
def get_next_id(curr_id):
	try:
		ret = Image.objects.filter(id__gt=curr_id).order_by("id")[0:1].get().id
	except Image.DoesNotExist:
		ret = Image.objects.aggregate(Min("id"))['id__min']
	return ret

def currency(euros):
    euros = round(float(euros), 2)
    return "€%s%s" % (intcomma(int(euros)), ("%0.2f" % euros)[-3:])

register.filter('currency', currency)