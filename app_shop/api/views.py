from rest_framework.response import Response
from app_shop.models import SpecialOffer, Product
from rest_framework.decorators import api_view
from app_shop.api.serializers import SpecialOfferSerializer, ProductSerializer, ProductRequestBodySerializer
from rest_framework.response import Response
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework.generics import ListAPIView
from rest_framework.pagination import PageNumberPagination
from django.db.models import Q
from django_filters.rest_framework import DjangoFilterBackend


# def serializer(qs):
#     res = []
#     for i in qs:
#         res.append({
#             'image': i.image.url,
#             'link': i.link,
#             'location': i.location,
#             'datetime': i.datetime
#         })
#     return res
    

@api_view()
def special_offer_list(request):
    """
    this is a test
    """
    qs = SpecialOffer.objects.last()
    serializer = SpecialOfferSerializer(qs)
    return Response({
        'result': serializer.data
    })


@api_view()
def product_detail(request, id):
    """
    Prodct Detail View
    """
    qs = Product.objects.get(id=id)
    serializer = ProductSerializer(qs)
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
    product = Product.objects.create(
        title='',
        sub_title='asd'
    )
    return Response(data={}, status=status.HTTP_201_CREATED)


class ProductListView(ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    pagination_class = PageNumberPagination
    filter_backends = [DjangoFilterBackend]

    def get_queryset(self):
        qs = super().get_queryset()
        title = self.request.GET.get('title')
        max_price = self.request.GET.get('max_price')
        min_price = self.request.GET.get('min_price')
        if max_price and min_price:
            qs = qs.filter(productcolor__price__gte=min_price, productcolor__price__lte=max_price)
        return qs.filter(
            Q(title__contains=title) | Q(sub_title__icontains=title)
        ) if title else qs

