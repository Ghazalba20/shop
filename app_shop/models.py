from django.db import models

# Create your models here.
class specialoffer(models.Model):
      image=models.ImageField()
      location=models.CharField()
      link=models.URLField()
      datetime=models.DateTimeField((""), auto_now=False, auto_now_add=False)
      def __str__(self):
            return str(self.title)


class product(models.Model):
      title= models.CharField(null=True,max_length=120)
 
      def __str__(self):
            return self.title
      
      
class product_color(models.Model):
         product=models.ForeignKey(product,on_delete=models.CASCADE)
         name=models.CharField(null=True ,max_length=120)
         color_code=models.CharField(null=True ,max_length=20)
         price=models.IntegerField(null=True)
         price_with_discount=models.CharField(null=True ,max_length=120)


         def __str__(self):
                return f'{self.product.title} + {self}'
         