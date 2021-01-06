from django.db import models
from django.template.defaultfilters import slugify
from django.utils import timezone
from django.urls import reverse
from django.urls import reverse

class Location(models.Model):
    name = models.CharField(max_length=30)

    class Meta: 
	    ordering = ('id',)
    def __str__(self):
        return self.name
    def get_absolute_url(self):
        return reverse('medical_home')	
		
class Specialism(models.Model):
    name = models.CharField(max_length=30)

    class Meta: 
	    ordering = ('id',)
    def __str__(self):
        return self.name
    def get_absolute_url(self):
        return reverse('medical_home')	

class Doctor(models.Model):
    name = models.CharField(max_length=30)
    specialism = models.ForeignKey(Specialism, on_delete=models.CASCADE)	

    class Meta: 
	    ordering = ('id',)
    def __str__(self):
        return self.name
    def get_absolute_url(self):
        return reverse('medical_home')	

class Consultation(models.Model):
	date = models.DateField(default=timezone.now)
	doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE,null=True)	
	specialism = models.ForeignKey(Specialism, on_delete=models.CASCADE,null=True)	
	location = models.ForeignKey(Location, on_delete=models.CASCADE,null=True)	
	description = models.CharField(max_length=1000,null=True)
	title = models.CharField(max_length=100,null=True)
	upsurge = models.CharField(max_length=50)

	class Meta: 
	    ordering = ('-date',)
	def __str__(self):
		return str(self.date)		
	def get_absolute_url(self):
		return reverse('medical_home', args=[self.date]+1)
		
class Medication(models.Model):
	start_date = models.DateField(default=timezone.now)
	end_date = models.DateField(default=timezone.now)
	medicatie = models.CharField(max_length=1000,null=True,default='Salozyprine')
	aantal_ochtend = models.IntegerField(blank=True,null=True,verbose_name='Ochtend:',default=0)
	aantal_avond = models.IntegerField(blank=True,null=True,verbose_name='Avond:',default=0)
	pijn = models.IntegerField(blank=True,null=True,verbose_name='Pijn-niveau (0,1,2,3):',default=0)
	opmerking = models.CharField(max_length=1000,null=True) 
	linkervoet = models.BooleanField("Linker voet",default=False)
	rechtervoet = models.BooleanField("Rechter voet",default=False)
	linkerhand = models.BooleanField("Linker hand",default=False)
	rechterhand = models.BooleanField("Rechter hand",default=False)
	rug = models.BooleanField("Rug",default=False)