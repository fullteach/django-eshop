from django.db.models.signals import pre_save,post_save,post_delete
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import *
@receiver(post_save,sender=User)
def customer_create(sender,instance,created,**kwargs):
    if created:
        user=instance
        customer=Customer.objects.create(user=user,name=user.username,email=user.email)

@receiver(post_delete,sender=Customer)
def customer_delete(sender,instance,**kwargs):
    user=instance.user
    user.delete()
    

@receiver(post_save,sender=Customer)
def order_create(sender,instance,created,**kwargs):
    if created:
        customer=instance
        import random
        number=random.randint(1000,9999)
        order=Order.objects.create(customer=customer,complete=False,transaction_id=number)
