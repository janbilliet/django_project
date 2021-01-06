from django import forms
from .models import Transaction, Category, Subcategory, Type, Picture
from .utils import OptionalChoiceField
from django.forms import ModelForm, Textarea
from .widgets import BootstrapDateTimePickerInput

class PostForm(forms.ModelForm):
    comment = forms.CharField(widget=forms.Textarea,required = False)
    class Meta:
        model = Transaction
        fields = ['date', 'type','category','subcategory','description','amount','comment','name']
        widgets = {
        'description': Textarea(attrs={'cols': 40, 'rows': 1}),
		'comment': Textarea(attrs={'cols': 40, 'rows': 2}),
        'date': forms.DateInput(format=('%Y-%m-%d'), attrs={'firstDay': 1, 'pattern=': '\d{4}-\d{2}-\d{2}', 'lang': 'pl', 'format': 'yyyy-mm-dd', 'type': 'date'}),		
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['category'].queryset = Category.objects.none()
        self.fields['subcategory'].queryset = Subcategory.objects.none()
		
        if 'type' in self.data:
            try:
                type_id = int(self.data.get('type'))
                self.fields['category'].queryset = Category.objects.filter(type_id=type_id).order_by('name')
            except (ValueError, TypeError):
                pass  # invalid input from the client; ignore and fallback to empty category queryset
        elif self.instance.pk:
            self.fields['category'].queryset = self.instance.type.category_set.order_by('name')
			
        if 'category' in self.data:
            try:
                category_id = int(self.data.get('category'))
                self.fields['subcategory'].queryset = Subcategory.objects.filter(category_id=category_id).order_by('name')
            except (ValueError, TypeError):
                pass  # invalid input from the client; ignore and fallback to empty category queryset
        elif self.instance.pk:
            self.fields['subcategory'].queryset = self.instance.category.subcategory_set.order_by('name')
			
class TypeForm(forms.ModelForm):
    class Meta:
        model = Type
        fields = ['name']

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['type','name']

class SubcategoryForm(forms.ModelForm):
    class Meta:
        model = Subcategory
        fields = ['category','name']

		
class PictureForm(forms.ModelForm):
    file = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': True}))
	 
    class Meta:
        model = Picture
        fields = ['transaction','file']