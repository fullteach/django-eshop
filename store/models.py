from tabnanny import verbose
from django.db import models
from django.contrib.auth.models import User
# CharField - max_length - 10,20
# TextField - nolimit -chegarisz
# IntegerField - raqamli   - 0 +
# PostiveField - raqamli 0 +
# DecimalField  - max_digit 
# FloatField - 8.98
# DateField - kun,sana
# TimeField vaqt
#DateTimeField kun yil oy sana vaqt
# auto_add -orgartirsak vaqt saqlanadi
# auto_now_add -boshida kiritilgan vaqt turadi 
# FileField - fayllar bilan ishlash
# ImageField rasmlar bilan ishlash
# Boolenfield - True,False
# null=True,blank=True Javob talab qilmaydi

# kalbasa sasiska pomidor
# pitsa somsa gamlet

# One to one Field
# ManytoManyField
# ForeignKey

# CASCADE , PROTECT , SET_NULL
# Create your models here.
class Customer(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE,db_constraint=False)
    name=models.CharField(max_length=200, null=True)
    email = models.CharField(max_length=200)
    # class Meta:
    #     verbose_name='Xaridor'
    #     verbose_name_plural='Xaridorlar'
    def __str__(self):
    		return self.name

class Product(models.Model):
			name = models.CharField(max_length=200)
			price = models.FloatField()
			digital = models.BooleanField(default=False,null=True, blank=True)
			image = models.ImageField(null=True, blank=True,upload_to='products')
			description=models.TextField(null=True,blank=True)
			def __str__(self):
					return self.name
			@property
			def ImageUrl(self):
				return self.image.url
		
class Order(models.Model):
			customer = models.ForeignKey(Customer, on_delete=models.CASCADE, null=True, blank=True,db_constraint=False)
			date_ordered = models.DateTimeField(auto_now_add=True)
			complete = models.BooleanField(default=False)
			transaction_id = models.CharField(max_length=100, null=True)
			def __str__(self):
					return self.customer.name
			@property
			def get_total_cart(self):
				orderitems=self.orderitem_set.all()
				total=sum([item.get_total for item in orderitems])
				return total
			@property
			def get_total_items(self):
				orderitems=self.orderitem_set.all()
				total=sum([item.quantity for item in orderitems])
				return total
		

class OrderItem(models.Model):
				product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True,db_constraint=False)
				order = models.ForeignKey(Order, on_delete=models.CASCADE, null=True,db_constraint=False)
				quantity = models.IntegerField(default=0, null=True, blank=True)
				date_added = models.DateTimeField(auto_now_add=True)
				def __str__(self):
						return f"{self.order.customer} {self.product.name} ni oldi"
				@property
				def get_total(self):
					total=self.product.price * self.quantity
					return total
		
	