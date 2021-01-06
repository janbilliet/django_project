from .models import DagboekPost, Image, Video
from django import forms

MijlpaalList = DagboekPost.objects.values_list('mijlpaal','mijlpaal').distinct().order_by('mijlpaal')
TitelList = DagboekPost.objects.values_list('titel','titel').distinct().order_by('titel')

class PostForm(forms.ModelForm):
    beschrijving = forms.CharField(widget=forms.Textarea)

    class Meta:
        model = DagboekPost
        fields = ['id','datum','titel', 'mijlpaal','sprong','titel','beschrijving','favpost','naam']
		
class ImageForm(forms.ModelForm):

    class Meta:
        model = Image
        fields = ['img','favimage','dagboekpost','name']
		
class VideoForm(forms.ModelForm):

    class Meta:
        model = Video
        fields = ['vid','favvideo','dagboekpost','name']