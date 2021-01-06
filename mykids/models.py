from django.db import models
from django.template.defaultfilters import slugify
from django.utils import timezone
from django.urls import reverse
from django.contrib.auth.models import User
from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFill,ResizeToFit,SmartResize
import datetime

class DagboekPost(models.Model):
    datum = models.DateField(default=timezone.now)
    SprongChoices = (
        ('S', 'Yes'),
        ('-', 'No'),
    )
    mijlpaal = models.CharField(blank=True,null=True,max_length=100)	
    sprong = models.BooleanField("Sprong", default=False)
    titel = models.CharField(blank=True,null=True,max_length=100)
    beschrijving = models.CharField(blank=True,null=True,max_length=7000)
    gewicht = models.DecimalField(blank=True,null=True,decimal_places=3,max_digits=5,default=0)
    lengte = models.DecimalField(blank=True,null=True,decimal_places=1,max_digits=4,default=0)
    uurvanOpstaan = models.DateTimeField(blank=True,null=True,default=timezone.now,verbose_name='Wakker geworden om:')
    uurvanSlapen = models.DateTimeField(blank=True,null=True,default=timezone.now,verbose_name='Gaan slapen om:')
    favpost = models.BooleanField("Favoriete post",default=False)
    nachtflesjes = models.IntegerField(blank=True,null=True,verbose_name='Aantal nachtflesjes:',default=0)
    naam = models.ForeignKey(User, on_delete=models.CASCADE,default=5)

    def count_days_lotte(self):
        return (self.datum - datetime.date(2019, 4, 22)).days + 1
		
    def count_days_bolleke(self):
        return (self.datum - datetime.date(2021, 6, 1)).days + 1
    
    daglotte = property(count_days_lotte)	
    dagbolleke = property(count_days_bolleke)		
	
    class Meta: 
        ordering = ('-id',)
    def __str__(self):
    	return str(self.id)
    def get_absolute_url(self):
        return reverse('mykids-detail', args=[str(self.id)])		


def generate_filename(self, filename):
    url = "mykids/%s/%s" % (self.name.username, filename)
    return url		
	
class Video(models.Model):
    vid = models.FileField(upload_to=generate_filename,blank=False,null=True)
    dagboekpost = models.ForeignKey(DagboekPost, default=None, on_delete=models.CASCADE)
    fav = models.BooleanField("Favoriet",default=False)
    alltimefav = models.BooleanField("All time fav",default=False)
    desc = models.CharField(blank=True,null=True,max_length=7000)
    order = models.IntegerField(blank=True,null=True,default=1)
    name = models.ForeignKey(User, on_delete=models.CASCADE)
	
    class Meta: 
	    ordering = ('dagboekpost',)
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
    fav = models.BooleanField("Favoriet",default=False)
    alltimefav = models.BooleanField("All time fav",default=False)
    desc = models.CharField(blank=True,null=True,max_length=7000)
    order = models.IntegerField(blank=True,null=True,default=1)
    name = models.ForeignKey(User, on_delete=models.CASCADE)
	
    class Meta: 
	    ordering = ('dagboekpost',)
    def __str__(self):
         return "{0} => {1}".format(self.id, self.dagboekpost)
    def get_absolute_url(self):
	     return reverse('mykids-image-detail', args=[str(self.id)])