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
