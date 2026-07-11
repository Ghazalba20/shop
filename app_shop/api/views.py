from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.http import JsonResponse
from app_shop.models import specialoffer,product
from app_shop.api.serializers import specialofferSerializer , productSerializer


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
