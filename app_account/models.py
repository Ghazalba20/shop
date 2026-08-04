from django.db import models
from django.contrib.auth.models import User
from app_shop.models import product
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType


# Create your models here.
class Userfavorite(models.Model):
    user=models.ForeignKey(User,on_delete=models.SET_NULL,null=True)
    content_type=models.ForeignKey(ContentType,on_delete=models.CASCADE,null=True)
    object_id=models.PositiveBigIntegerField(null=True)
    content_obj=GenericForeignKey("content_type","object_id")

    def __str__(self):
        return f'{self.user}{self.content_type}{self.object_id}'
    


class Profile(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE,related_name='profile')
    phone_number=models.CharField(max_length=15,unique=True,null=True)
    is_phone_verified=models.BooleanField(default=False)
    first_name=models.CharField(max_length=120,null=True,blank=True)
    last_name=models.CharField(max_length=120,null=True,blank=True)

    def __str__(self):
        return f'{self.phone_number}'

class PhoneVerificationCode(models.Model):
    phone_number=models.CharField(max_length=15)
    code=models.CharField(max_length=6)
    created_at=models.DateTimeField(auto_now_add=True)
    is_used=models.BooleanField(default=False)

    def __str__(self):
        return f'{self.phone_number} - {self.code}'


class Address(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE,related_name='addresses')
    title=models.CharField(max_length=120,null=True)
    province=models.CharField(max_length=120,null=True)
    city=models.CharField(max_length=120,null=True)
    address=models.TextField(null=True)
    postal_code=models.CharField(max_length=20,null=True)
    receiver_name=models.CharField(max_length=120,null=True)
    receiver_phone=models.CharField(max_length=15,null=True)


 
class Basket(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE,related_name='basket')

    def __str__(self):
        return f'basket-{self.user}'


class BasketItem(models.Model):
    basket=models.ForeignKey(Basket,on_delete=models.CASCADE,related_name='items')
    product_color=models.ForeignKey('app_shop.product_color',on_delete=models.CASCADE)
    quantity=models.PositiveIntegerField(default=1)

    def __str__(self):
        return f'{self.basket.user} - {self.product_color} x {self.quantity}'
      