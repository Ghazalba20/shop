from django.contrib import admin
from app_account.models import Userfavorite , Profile,Address,PhoneVerificationCode

admin.site.register(Userfavorite)
admin.site.register(Profile)
admin.site.register(PhoneVerificationCode)
admin.site.register(Address)
