from .models import DagboekPost, Video, Image, Mijlpaal, Tag
from django import forms
from django.forms import ModelForm, Textarea
from .widgets import BootstrapDateTimePickerInput

class PostForm(forms.ModelForm):

    class Meta:
        model = DagboekPost
        fields = ['id','datum','titel_lotte','titel_merlijn','mijlpaal','beschrijving_lotte','beschrijving_merlijn','favpost']
        widgets = {
        'beschrijving_lotte': Textarea(attrs={'cols': 80, 'rows': 5}),
        'beschrijving_merlijn': Textarea(attrs={'cols': 80, 'rows': 5}),
        'datum': forms.DateInput(format=('%Y-%m-%d'), attrs={'firstDay': 1, 'pattern=': '\d{4}-\d{2}-\d{2}', 'lang': 'pl', 'format': 'yyyy-mm-dd', 'type': 'date'}),		
        }
		
class VideoForm(forms.ModelForm):
    vid = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': True}))	
	
    class Meta:
        model = Video
        fields = ['rating','dagboekpost','order','desc','vid','vidlotte','vidmerlijn','vidpapa','vidmama']
		
class ImageForm(forms.ModelForm):
    img = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': True}))
	
    class Meta:
        model = Image
        fields = ['rating','dagboekpost','order','desc','img','imglotte','imgmerlijn','imgpapa','imgmama']

class MijlpaalForm(forms.ModelForm):
    class Meta:
        model = Mijlpaal
        fields = ['name']

class TagForm(forms.ModelForm):
    class Meta:
        model = Tag
        fields = ['name']