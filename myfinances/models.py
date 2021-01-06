from django.db import models
from django.utils import timezone
from django.urls import reverse
from django.contrib.auth.models import User

class Type(models.Model):
    name = models.CharField(max_length=30)

    class Meta: 
	    ordering = ('name',)
    def __str__(self):
        return self.name
    def get_absolute_url(self):
        return reverse('transaction_home')	
		
class Category(models.Model):
    name = models.CharField(max_length=30)
    type = models.ForeignKey(Type, on_delete=models.CASCADE)

    class Meta: 
	    ordering = ('name',)
    def __str__(self):
        return self.name
    def get_absolute_url(self):
        return reverse('transaction_home')	

class Subcategory(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    name = models.CharField(max_length=30)

    class Meta: 
	    ordering = ('name',)
    def __str__(self):
        return self.name
    def get_absolute_url(self):
        return reverse('transaction_home')	

class Transaction(models.Model):
	date = models.DateField(default=timezone.now)
	type = models.ForeignKey(Type, on_delete=models.SET_NULL, null=True)
	category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
	subcategory = models.ForeignKey(Subcategory, on_delete=models.SET_NULL, null=True)
	description = models.CharField(blank=True,null=True,max_length=1000)
	amount	= models.FloatField(blank=True,null=True, default=0)
	comment = models.CharField(blank=True,null=True,max_length=1000)
	name = models.ForeignKey(User, on_delete=models.CASCADE)

	class Meta: 
	    ordering = ('-date',)
	def __str__(self):
		return str(self.id)
	def get_absolute_url(self):
		return reverse('transaction_home')	
		
class Picture(models.Model):
    file = models.FileField(upload_to='myfinances/',blank=False,null=True)
    transaction = models.ForeignKey(Transaction, default=None, on_delete=models.CASCADE)
	
    class Meta: 
	    ordering = ('-id',)
    def get_absolute_url(self):
	     return reverse('transaction_detail', args=[str(self.id)])