from app_account.models import Userfavorite
from rest_framework import serializers


class userfavoriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Userfavorite
        fields='__all__'
