from django.contrib import admin
from .models import *


# Register your models here.

admin.site.register(Profile)
admin.site.register(Cart)
admin.site.register(CartItem)
admin.site.register(Variation)

admin.site.register(Order)
