from .models import DagboekPost, Image, Video, Rating
from django import forms

class PostForm(forms.ModelForm):
    beschrijving = forms.CharField(widget=forms.Textarea)

    class Meta:
        model = DagboekPost
        fields = ['id','datum','titel_lotte', 'titel_merlijn', 'mijlpaal', 'mijlpaal_merlijn','beschrijving_lotte','beschrijving_merlijn','favpost']
		
class ImageForm(forms.ModelForm):

    class Meta:
        model = Image
        fields = ['img','rating','dagboekpost','imglotte','imgmerlijn','imgpapa','imgmama']
		
class VideoForm(forms.ModelForm):

    class Meta:
        model = Video
        fields = ['vid','rating','dagboekpost','vidlotte','vidmerlijn','vidpapa','vidmama']