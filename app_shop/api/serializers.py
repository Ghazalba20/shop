from app_shop.models import specialoffer,product,product_color
from rest_framework import serializers

class specialofferSerializer(serializers.ModelSerializer):
    image=serializers.SerializerMethodField()

    def get_image(self,obj):
         return'https://localhost:8000' + obj.image.url

         
    class Meta:
        model = specialoffer
        # fields = ["id", "image", "link", "location","datetime"]
        exclude=('datetime','id')



class product_color_serializer(serializers.ModelSerializer):
    class Meta:
        model=product_color
        fields='__all__'


class productSerializer(serializers.ModelSerializer):
    hi=serializers.SerializerMethodField()
    def get_hi(self,obj):
        qs=obj.product_color_set.all()
        serializer=product_color_serializer(qs,many=True)
        return serializer.data
    class Meta:
        model = product
        fields='__all__'


class ProductRequestBodySerializer(serializers.Serializer):
    title=serializers.CharField()
    sub_title=serializers.CharField()