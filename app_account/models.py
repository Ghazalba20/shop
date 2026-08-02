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
    

