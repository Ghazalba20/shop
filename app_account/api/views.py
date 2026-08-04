from rest_framework.response import Response
from rest_framework.decorators import api_view,authentication_classes,permission_classes
from rest_framework.permissions import IsAuthenticated
from app_account.models import Userfavorite,Profile,PhoneVerificationCode,Address,Basket,BasketItem,Order,OrderItem
from app_account.api.serializers import userfavoriteSerializer, UserFavoriteRequestBodySerializer,ProfileSerializer,ProfileUpdateRequestBodySerializer,RegisterRequestBodySerializer,ResendCodeRequestBodySerializer,VerifyRequestBodySerializer
from app_account.api.serializers import AddressSerializer ,BasketItemSerializer,AddToBasketRequestBodySerializer,RemoveFromBasketRequestBodySerializer
from django.contrib.contenttypes.models import ContentType
from app_account.api.serializers import OrderItemSerializer,OrderSerializer,PurchaseRequestBodySerializer
from rest_framework.response import Response
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework_simplejwt.authentication import JWTAuthentication



@api_view()
def favorite_list(request):
    """
    Favorite list View
    """
    qs = Userfavorite.objects.all()
    serializer = userfavoriteSerializer(qs, many=True)
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
    request_body=UserFavoriteRequestBodySerializer,
)
@api_view(['POST'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])

def favorite(request):
    """
    Favorite list View
    """
    serializer = UserFavoriteRequestBodySerializer(data=request.POST)
    user_id = request.user.id

    try:
        if serializer.is_valid():
            object_id = serializer.data['object_id']
            object_type = serializer.data['object_type']
            product_ct = ContentType.objects.get(model=object_type)
        # else:
        #     return somethong
    except ContentType.DoesNotExist:
        data = {
            'message': 'Invalid Content Type!',
            'status': 'not ok'
        }
        return Response(data=data, status=status.HTTP_404_NOT_FOUND)
    user_favorite = None
    fields = {
        'user_id': user_id,
        'object_id': object_id,
        'content_type': product_ct
    }
    user_favorite, created = Userfavorite.objects.get_or_create(**fields)
    if created:
        # create if doe's not exist
        return Response(data={'status': 'ok'}, status=status.HTTP_201_CREATED)
    else:
        # delete if exists
        user_favorite.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    

    


@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def profile_detail(request):
    """
    personal info detail
    """
    profile = request.user.profile
    serializer = ProfileSerializer(profile)
    return Response({'result': serializer.data})


@swagger_auto_schema(
    method='put',
    responses={200: 'updated'},
    request_body=ProfileUpdateRequestBodySerializer,
)
@api_view(['PUT'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def profile_update(request):
    """
    update personal info
    """
    profile = request.user.profile
    profile.first_name = request.data.get('first_name', profile.first_name)
    profile.last_name = request.data.get('last_name', profile.last_name)
    profile.save()
    return Response(data=ProfileSerializer(profile).data, status=status.HTTP_200_OK)


def _generate_code():
    return str(random.randint(1000, 9999))


@swagger_auto_schema(
    method='post',
    responses={
        200: 'code sent',
        400: 'invalid data',
    },
    request_body=RegisterRequestBodySerializer,
)
@api_view(['POST'])
def register(request):
    """
    register with phone number, creates an inactive user + profile and sends a code
    """
    serializer = RegisterRequestBodySerializer(data=request.data)
    if not serializer.is_valid():
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    phone_number = serializer.data['phone_number']

    user, _ = User.objects.get_or_create(username=phone_number)
    profile, _ = Profile.objects.get_or_create(user=user, defaults={'phone_number': phone_number})

    code = _generate_code()
    PhoneVerificationCode.objects.create(phone_number=phone_number, code=code)

    # sending sms is not implemented, code is printed instead
    print(f'verification code for {phone_number} is {code}')

    return Response(data={'message': 'code sent'}, status=status.HTTP_200_OK)


@swagger_auto_schema(
    method='post',
    responses={
        200: 'verified',
        400: 'invalid code',
        404: 'user not found',
    },
    request_body=VerifyRequestBodySerializer,
)
@api_view(['POST'])
def verify(request):
    """
    verify phone number with the sent code
    """
    serializer = VerifyRequestBodySerializer(data=request.data)
    if not serializer.is_valid():
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    phone_number = serializer.data['phone_number']
    code = serializer.data['code']

    try:
        user = User.objects.get(username=phone_number)
    except User.DoesNotExist:
        return Response(data={'message': 'user not found'}, status=status.HTTP_404_NOT_FOUND)

    verification = PhoneVerificationCode.objects.filter(
        phone_number=phone_number, code=code, is_used=False
    ).order_by('-created_at').first()

    if not verification:
        return Response(data={'message': 'invalid code'}, status=status.HTTP_400_BAD_REQUEST)

    verification.is_used = True
    verification.save()

    user.is_active = True
    user.save()

    profile = user.profile
    profile.is_phone_verified = True
    profile.save()

    Basket.objects.get_or_create(user=user)

    refresh = RefreshToken.for_user(user)
    return Response(data={
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }, status=status.HTTP_200_OK)


@swagger_auto_schema(
    method='post',
    responses={
        200: 'code resent',
        404: 'user not found',
    },
    request_body=ResendCodeRequestBodySerializer,
)
@api_view(['POST'])
def resend_code(request):
    """
    resend verification code
    """
    serializer = ResendCodeRequestBodySerializer(data=request.data)
    if not serializer.is_valid():
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    phone_number = serializer.data['phone_number']

    if not User.objects.filter(username=phone_number).exists():
        return Response(data={'message': 'user not found'}, status=status.HTTP_404_NOT_FOUND)

    code = _generate_code()
    PhoneVerificationCode.objects.create(phone_number=phone_number, code=code)
    print(f'verification code for {phone_number} is {code}')

    return Response(data={'message': 'code resent'}, status=status.HTTP_200_OK)


# profile

@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def profile_detail(request):
    """
    personal info detail
    """
    profile = request.user.profile
    serializer = ProfileSerializer(profile)
    return Response({'result': serializer.data})


@swagger_auto_schema(
    method='put',
    responses={200: 'updated'},
    request_body=ProfileUpdateRequestBodySerializer,
)
@api_view(['PUT'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def profile_update(request):
    """
    update personal info
    """
    profile = request.user.profile
    profile.first_name = request.data.get('first_name', profile.first_name)
    profile.last_name = request.data.get('last_name', profile.last_name)
    profile.save()
    return Response(data=ProfileSerializer(profile).data, status=status.HTTP_200_OK)



# address
@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def address_list(request):
    """
    list user addresses
    """
    qs = Address.objects.filter(user=request.user)
    serializer = AddressSerializer(qs, many=True)
    return Response({'result': serializer.data})


@swagger_auto_schema(
    method='post',
    responses={201: 'created', 400: 'invalid data'},
    request_body=AddressSerializer,
)
@api_view(['POST'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def address_add(request):
    """
    add a new address
    """
    serializer = AddressSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(user=request.user)
        return Response(data=serializer.data, status=status.HTTP_201_CREATED)
    return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@swagger_auto_schema(
    method='put',
    responses={200: 'updated', 404: 'not found'},
    request_body=AddressSerializer,
)
@api_view(['PUT'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def address_update(request, id):
    """
    update an address
    """
    try:
        address = Address.objects.get(id=id, user=request.user)
    except Address.DoesNotExist:
        return Response(data={'message': 'not found'}, status=status.HTTP_404_NOT_FOUND)

    serializer = AddressSerializer(address, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(data=serializer.data, status=status.HTTP_200_OK)
    return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def address_remove(request, id):
    """
    remove an address
    """
    try:
        address = Address.objects.get(id=id, user=request.user)
    except Address.DoesNotExist:
        return Response(data={'message': 'not found'}, status=status.HTTP_404_NOT_FOUND)
    address.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)

#basket 
@swagger_auto_schema(
    method='post',
    responses={201: 'added', 400: 'invalid data', 404: 'product color not found'},
    request_body=AddToBasketRequestBodySerializer,
)
@api_view(['POST'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def add_to_basket(request):
    """
    add item to basket
    """
    serializer = AddToBasketRequestBodySerializer(data=request.data)
    if not serializer.is_valid():
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    try:
        color = product_color.objects.get(id=serializer.data['product_color'])
    except product_color.DoesNotExist:
        return Response(data={'message': 'product color not found'}, status=status.HTTP_404_NOT_FOUND)

    basket, _ = Basket.objects.get_or_create(user=request.user)
    item, created = BasketItem.objects.get_or_create(
        basket=basket, product_color=color,
        defaults={'quantity': serializer.data['quantity']},
    )
    if not created:
        item.quantity += serializer.data['quantity']
        item.save()

    return Response(data=BasketItemSerializer(item).data, status=status.HTTP_201_CREATED)


@swagger_auto_schema(
    method='post',
    responses={204: 'removed', 404: 'not found'},
    request_body=RemoveFromBasketRequestBodySerializer,
)
@api_view(['POST'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def remove_from_basket(request):
    """
    remove item from basket
    """
    serializer = RemoveFromBasketRequestBodySerializer(data=request.data)
    if not serializer.is_valid():
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    try:
        basket = Basket.objects.get(user=request.user)
        item = BasketItem.objects.get(basket=basket, product_color_id=serializer.data['product_color'])
    except (Basket.DoesNotExist, BasketItem.DoesNotExist):
        return Response(data={'message': 'not found'}, status=status.HTTP_404_NOT_FOUND)

    item.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def basket_detail(request):
    """
    current user's basket
    """
    basket, _ = Basket.objects.get_or_create(user=request.user)
    serializer = BasketItemSerializer(basket.items.all(), many=True)
    return Response({'result': serializer.data})


#purchase 
@swagger_auto_schema(
    method='post',
    responses={201: 'order created', 400: 'basket is empty'},
    request_body=PurchaseRequestBodySerializer,
)
@api_view(['POST'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def purchase(request):
    """
    checkout the basket and create an order
    """
    serializer = PurchaseRequestBodySerializer(data=request.data)
    if not serializer.is_valid():
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    try:
        basket = Basket.objects.get(user=request.user)
    except Basket.DoesNotExist:
        return Response(data={'message': 'basket is empty'}, status=status.HTTP_400_BAD_REQUEST)

    items = basket.items.all()
    if not items:
        return Response(data={'message': 'basket is empty'}, status=status.HTTP_400_BAD_REQUEST)

    total_price = 0
    order = Order.objects.create(user=request.user, address_id=serializer.data['address'])
    for item in items:
        price = item.product_color.price or 0
        OrderItem.objects.create(
            order=order, product_color=item.product_color,
            quantity=item.quantity, price=price,
        )
        total_price += price * item.quantity

    order.total_price = total_price
    order.status = 'paid'
    order.save()

    items.delete()

    return Response(data=OrderSerializer(order).data, status=status.HTTP_201_CREATED)


@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def order_list(request):
    """
    list current user's orders
    """
    qs = Order.objects.filter(user=request.user).order_by('-created_at')
    serializer = OrderSerializer(qs, many=True)
    return Response({'result': serializer.data})


@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def order_detail(request, id):
    """
    current user's order detail
    """
    try:
        order = Order.objects.get(id=id, user=request.user)
    except Order.DoesNotExist:
        return Response(data={'message': 'not found'}, status=status.HTTP_404_NOT_FOUND)
    return Response({'result': OrderSerializer(order).data})
