from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.http import JsonResponse
from app_shop.models import specialoffer,product
from app_shop.api.serializers import specialofferSerializer , productSerializer,ProductRequestBodySerializer
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.contrib.contenttypes.models import ContentType
from rest_framework.response import Response
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi


@api_view()


# def specialoffer(request):
#     return JsonResponse({
     #     'result':specialoffer.object.all()
#     })

@api_view()
def special_offer_list(request):
    qs=specialoffer.objects.all()
    serializer=specialofferSerializer(qs, many=True)
    return Response({
        'result': serializer.data
    })

@api_view()
def product_detail(request,id):
    '''
    product details view
    '''
    qs=specialoffer.objects.get(id=id)
    serializer=productSerializer(qs, many=True)
    return Response({
        'result': serializer.data
    })




@api_view()
def favorite_list(request):
    """
    Favorite list View
    """
    qs = UserFavorite.objects.all()
    serializer = UserFavoriteSerializer(qs, many=True)
    return Response({
        'result': serializer.data
    })


@swagger_auto_schema(
    method='post',
    responses={
        201: 'create favorite', 
        204: 'delete favorite',
        400: 'invalid number',
        404: 'content type not found',
    },
    request_body=ProductRequestBodySerializer,
)
@api_view(['POST'])
def product_create(request):
    """
    product create

    """
  
    product = product.objects.create(
       title='',
       sub_title='asd' 
    )
    return Response(data={},status=status.HTTP_201_CREATED)
