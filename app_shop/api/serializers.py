from app_shop.models import specialoffer,product,product_color,comment
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
    colors = serializers.SerializerMethodField()

    def get_colors(self, obj):
        qs = obj.productcolor_set.all()
        serializer = product_color_serializer(qs, many=True)
        return serializer.data

    class Meta:
        model = product
        fields = '__all__'


class ProductRequestBodySerializer(serializers.Serializer):
    title=serializers.CharField()


class ProductCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model=product
        fields=['title']


class commentSerializer(serializers.ModelSerializer):
    user=serializers.StringRelatedField(read_only=True)
    class Meta:
        model=comment
        fields=['id','product','user','text','created_at','updated_at']
        read_only_fields=['user','created_at','updated_at']


class CommentRequestBodySerializer(serializers.Serializer):
    product=serializers.IntegerField()
    text=serializers.CharField()