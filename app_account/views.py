from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.http import JsonResponse
from app_account.models import Userfavorite
from app_account.api.serializers import userfavoriteSerializer



@api_view()
def favorite_list(request):
    '''
    favorite list view
    '''
    qs=Userfavorite.objects.all()
    serializer=userfavoriteSerializer(qs, many=True)
    return Response({
        'result': serializer.data
    })
 