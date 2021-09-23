from django.db import models
from django.template.defaultfilters import slugify
from django.utils import timezone
from django.urls import reverse
from django.contrib.auth.models import User
from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFill,ResizeToFit,SmartResize
import datetime


class Mijlpaal(models.Model):
    name = models.CharField(max_length=30, null=True)

    class Meta: 
	    ordering = ('id',)
    def __str__(self):
        return self.name
    def get_absolute_url(self):
        return reverse('mykids-home-list')	

class Rating(models.Model):
    name = models.CharField(max_length=30, null=True)

    class Meta: 
	    ordering = ('id',)
    def __str__(self):
        return self.name
    def get_absolute_url(self):
        return reverse('mykids-home-list')	

class Tag(models.Model):
    name = models.CharField(max_length=30, null=True)

    class Meta: 
	    ordering = ('id',)
    def __str__(self):
        return self.name
    def get_absolute_url(self):
        return reverse('mykids-home-list')	

class DagboekPost(models.Model):
    datum = models.DateField(default=timezone.now)
    mijlpaal = models.ForeignKey(Mijlpaal, on_delete=models.SET_NULL, null=True)
    titel_lotte = models.CharField(blank=True,null=True,max_length=100)
    titel_merlijn = models.CharField(blank=True,null=True,max_length=100)
    beschrijving_lotte = models.CharField(blank=True,null=True,max_length=7000)
    beschrijving_merlijn = models.CharField(blank=True,null=True,max_length=7000) 
    favpost = models.BooleanField("Favoriete post",default=False)

    def count_days_lotte(self):
        return (self.datum - datetime.date(2019, 4, 22)).days + 1
		
    def count_days_merlijn(self):
        return (self.datum - datetime.date(2021, 6, 7)).days + 1
    
    daglotte = property(count_days_lotte)	

    dagmerlijn = property(count_days_merlijn)		
	
    class Meta: 
        ordering = ('-datum',)
    def __str__(self):
    	return str(self.id)
    def get_absolute_url(self):
        return reverse('mykids-detail', args=[str(self.id)])		


def generate_filename(self, filename):
    url = "mykids/%s/%s" % (self.rating, filename)
    return url		
	
class Video(models.Model):
    vid = models.FileField(upload_to=generate_filename,blank=False,null=True)
    dagboekpost = models.ForeignKey(DagboekPost, default=None, on_delete=models.CASCADE)
    rating = models.ForeignKey(Rating, on_delete=models.SET_NULL, null=True)
    desc = models.CharField(blank=True,null=True,max_length=7000)
    order = models.IntegerField(blank=True,null=True,default=1)
    vidlotte = models.BooleanField("Lotte",default=False)
    vidmerlijn = models.BooleanField("Merlijn",default=False)
    vidpapa = models.BooleanField("Papa",default=False)
    vidmama = models.BooleanField("Mama",default=False)
	
    class Meta: 
	    ordering = ('-dagboekpost__datum',)
    def __str__(self):
         return "{0} => {1}".format(self.id, self.dagboekpost)
    def get_absolute_url(self):
	     return reverse('mykids-video-detail', args=[str(self.id)])
		 
class Image(models.Model):
    img = models.ImageField(upload_to=generate_filename,blank=False,null=True)
    img_thumbnail = ImageSpecField(source='img',
                                      processors=[ResizeToFill(width=200,height=200)],
                                      format='JPEG',
                                      options={'quality': 60})
    img_preview = ImageSpecField(source='img',
                                      processors=[SmartResize(width=1000,height=1000)],
                                      format='JPEG',
                                      options={'quality': 60})	
    dagboekpost = models.ForeignKey(DagboekPost, default=None, on_delete=models.CASCADE)
    rating = models.ForeignKey(Rating, on_delete=models.SET_NULL, null=True)
    desc = models.CharField(blank=True,null=True,max_length=7000)
    order = models.IntegerField(blank=True,null=True,default=1)
    imglotte = models.BooleanField("Lotte",default=False)
    imgmerlijn = models.BooleanField("Merlijn",default=False)
    imgpapa = models.BooleanField("Papa",default=False)
    imgmama = models.BooleanField("Mama",default=False)
	
	
    class Meta: 
	    ordering = ('-id',)
    def __str__(self):
         return "{0} => {1}".format(self.id, self.dagboekpost)
    def get_absolute_url(self):
	     return reverse('mykids-image-detail', args=[str(self.id)])
