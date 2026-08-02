from app_account.models import Userfavorite
from rest_framework import serializers


class userfavoriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Userfavorite
        fields='__all__'

class UserFavoriteRequestBodySerializer(serializers.Serializer):
    object_id = serializers.IntegerField()
    object_type = serializers.CharField()
