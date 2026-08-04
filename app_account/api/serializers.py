from app_account.models import Userfavorite,Address,Profile
from rest_framework import serializers


class userfavoriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Userfavorite
        fields='__all__'

class UserFavoriteRequestBodySerializer(serializers.Serializer):
    object_id = serializers.IntegerField()
    object_type = serializers.CharField()




class ProfileSerializer(serializers.ModelSerializer):
   class Meta:
        model=Profile
        fields=['id','phone_number','is_phone_verified','first_name','last_name']
        read_only_fields=['phone_number','is_phone_verified']


class ProfileUpdateRequestBodySerializer(serializers.Serializer):
    first_name=serializers.CharField(required=False)
    last_name=serializers.CharField(required=False)


class RegisterRequestBodySerializer(serializers.Serializer):
    phone_number=serializers.CharField()


class VerifyRequestBodySerializer(serializers.Serializer):
    phone_number=serializers.CharField()
    code=serializers.CharField()


class ResendCodeRequestBodySerializer(serializers.Serializer):
    phone_number=serializers.CharField()




class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model=Address
        fields=['id','title','province','city','address','postal_code','receiver_name','receiver_phone']
