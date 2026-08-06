from rest_framework.decorators import api_view,authentication_classes,permission_classes
from rest_framework.response import Response
from django.http import JsonResponse
from django.db.models import Q
from app_shop.models import specialoffer,product,product_color,comment
from app_shop.api.serializers import (
    specialofferSerializer , ProductSerializer,ProductRequestBodySerializer,
    ProductCreateSerializer,commentSerializer,CommentRequestBodySerializer
)
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.contrib.contenttypes.models import ContentType
from rest_framework.response import Response
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework.permissions import IsAuthenticated,IsAdminUser
from rest_framework_simplejwt.authentication import JWTAuthentication


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
    qs=product.objects.get(id=id)
    serializer=productSerializer(qs)
    return Response({
        'result': serializer.data
    })


@api_view()
def product_list(request):
    """
    product list view + search + filter
    query params:
        search -> search in title
        min_price , max_price -> filter by product_color price
    """
    qs=product.objects.all()
    search=request.GET.get('search')
    if search:
        qs=qs.filter(title__icontains=search)

    min_price=request.GET.get('min_price')
    max_price=request.GET.get('max_price')
    if min_price:
        qs=qs.filter(product_color__price__gte=min_price)
    if max_price:
        qs=qs.filter(product_color__price__lte=max_price)

    qs=qs.distinct()
    serializer=productSerializer(qs, many=True)
    return Response({
        'result': serializer.data
    })


@swagger_auto_schema(
    method='post',
    responses={
        201: 'product created',
        400: 'invalid data',
    },
    request_body=ProductCreateSerializer,
)
@api_view(['POST'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAdminUser])
def product_create(request):
    """
    product create - only site admin
    """
    serializer=ProductCreateSerializer(data=request.data)
    if serializer.is_valid():
        new_product=serializer.save()
        return Response(data=productSerializer(new_product).data,status=status.HTTP_201_CREATED)
    return Response(data=serializer.errors,status=status.HTTP_400_BAD_REQUEST)


@swagger_auto_schema(
    method='put',
    responses={
        200: 'product updated',
        400: 'invalid data',
        404: 'not found',
    },
    request_body=ProductCreateSerializer,
)
@api_view(['PUT'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAdminUser])
def product_update(request,id):
    """
    product update - only site admin
    """
    try:
        product_obj=product.objects.get(id=id)
    except product.DoesNotExist:
        return Response(data={'message':'not found'},status=status.HTTP_404_NOT_FOUND)

    serializer=ProductCreateSerializer(product_obj,data=request.data,partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(data=productSerializer(product_obj).data,status=status.HTTP_200_OK)
    return Response(data=serializer.errors,status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAdminUser])
def product_delete(request,id):
    """
    product delete - only site admin
    """
    try:
        product_obj=product.objects.get(id=id)
    except product.DoesNotExist:
        return Response(data={'message':'not found'},status=status.HTTP_404_NOT_FOUND)
    product_obj.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)


@api_view()
def comment_list(request,product_id):
    """
    list comments of a product
    """
    qs=comment.objects.filter(product_id=product_id).order_by('-created_at')
    serializer=commentSerializer(qs,many=True)
    return Response({
        'result': serializer.data
    })


@swagger_auto_schema(
    method='post',
    responses={
        201: 'comment created',
        400: 'invalid data',
    },
    request_body=CommentRequestBodySerializer,
)
@api_view(['POST'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def comment_create(request):
    """
    comment create
    """
    serializer=CommentRequestBodySerializer(data=request.data)
    if serializer.is_valid():
        new_comment=comment.objects.create(
            product_id=serializer.data['product'],
            user=request.user,
            text=serializer.data['text'],
        )
        return Response(data=commentSerializer(new_comment).data,status=status.HTTP_201_CREATED)
    return Response(data=serializer.errors,status=status.HTTP_400_BAD_REQUEST)


@swagger_auto_schema(
    method='put',
    responses={
        200: 'comment updated',
        400: 'invalid data',
        403: 'not allowed',
        404: 'not found',
    },
    request_body=CommentRequestBodySerializer,
)
@api_view(['PUT'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def comment_update(request,id):
    """
    comment update - only owner
    """
    try:
        comment_obj=comment.objects.get(id=id)
    except comment.DoesNotExist:
        return Response(data={'message':'not found'},status=status.HTTP_404_NOT_FOUND)

    if comment_obj.user_id != request.user.id:
        return Response(data={'message':'not allowed'},status=status.HTTP_403_FORBIDDEN)

    comment_obj.text=request.data.get('text',comment_obj.text)
    comment_obj.save()
    return Response(data=commentSerializer(comment_obj).data,status=status.HTTP_200_OK)


@api_view(['DELETE'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def comment_delete(request,id):
    """
    comment delete - only owner
    """
    try:
        comment_obj=comment.objects.get(id=id)
    except comment.DoesNotExist:
        return Response(data={'message':'not found'},status=status.HTTP_404_NOT_FOUND)

    if comment_obj.user_id != request.user.id:
        return Response(data={'message':'not allowed'},status=status.HTTP_403_FORBIDDEN)

    comment_obj.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)
