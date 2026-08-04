from django.contrib import admin
from app_account.models import Userfavorite , Profile,Address,PhoneVerificationCode
from app_account.models import Basket,BasketItem

admin.site.register(Userfavorite)
admin.site.register(Profile)
admin.site.register(PhoneVerificationCode)
admin.site.register(Address)
admin.site.register(Basket)
admin.site.register(BasketItem)
