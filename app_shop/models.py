from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class specialoffer(models.Model):
      image=models.ImageField()
      location=models.CharField()
      link=models.URLField()
      datetime=models.DateTimeField((""), auto_now=False, auto_now_add=False)
      def __str__(self):
            return str(self.datetime)


class product(models.Model):
      title= models.CharField(null=True,max_length=120)
 
      def __str__(self):
            return self.title
      
      

class product_color(models.Model):
    product = models.ForeignKey(product, on_delete=models.CASCADE)
    name = models.CharField(null=True, max_length=20)
    color_code = models.CharField(null=True, max_length=7)
    price = models.IntegerField(null=True)
    price_with_discount = models.IntegerField(null=True)

    def __str__(self):
        return f'{self.product.title} {self.name}'
         


class comment(models.Model):
      product=models.ForeignKey(product,on_delete=models.CASCADE,related_name='comments')
      user=models.ForeignKey(User,on_delete=models.SET_NULL,null=True)
      text=models.TextField(null=True)
      created_at=models.DateTimeField(auto_now_add=True)
      updated_at=models.DateTimeField(auto_now=True)

      def __str__(self):
            return f'{self.user} - {self.product.title}'