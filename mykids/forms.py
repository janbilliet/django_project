from .models import DagboekPost, Video, Image, Mijlpaal, Tag
from django import forms
from django.forms import ModelForm, Textarea
from .widgets import BootstrapDateTimePickerInput

MijlpaalList = DagboekPost.objects.values_list('mijlpaal','mijlpaal').distinct().order_by('mijlpaal')
TitelList = DagboekPost.objects.values_list('titel','titel').distinct().order_by('titel')

class PostForm(forms.ModelForm):
    # uurvanOpstaan = forms.DateTimeField(input_formats=['YYYY-MM-DD HH:MM:SS'],widget=BootstrapDateTimePickerInput())
    # uurvanSlapen = forms.DateTimeField(input_formats=['YYYY-MM-DD HH:MM:SS'],widget=BootstrapDateTimePickerInput())
    # uur1 = forms.DateTimeField(input_formats=['YYYY-MM-DD HH:MM:SS'],widget=BootstrapDateTimePickerInput())

    class Meta:
        model = DagboekPost
        fields = ['id','datum','titel','mijlpaal','beschrijving','favpost','sprong','uurvanOpstaan','uurvanSlapen','nachtflesjes','lengte','gewicht','tag']
        widgets = {
        'beschrijving': Textarea(attrs={'cols': 80, 'rows': 5}),
        'datum': forms.DateInput(format=('%Y-%m-%d'), attrs={'firstDay': 1, 'pattern=': '\d{4}-\d{2}-\d{2}', 'lang': 'pl', 'format': 'yyyy-mm-dd', 'type': 'date'}),		
        }
		
class VideoForm(forms.ModelForm):
    vid = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': True}))	
	
    class Meta:
        model = Video
        fields = ['name','dagboekpost','order','desc','vid','fav','alltimefav']
		
class ImageForm(forms.ModelForm):
    img = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': True}))
	
    class Meta:
        model = Image
        fields = ['name','dagboekpost','order','img','desc','fav','alltimefav']

class MijlpaalForm(forms.ModelForm):
    class Meta:
        model = Mijlpaal
        fields = ['name']

class TagForm(forms.ModelForm):
    class Meta:
        model = Tag
        fields = ['name']