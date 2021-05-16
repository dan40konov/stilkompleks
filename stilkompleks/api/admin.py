from django.contrib import admin
from .models import *
# Register your models here.
admin.site.register(Obekti)
admin.site.register(Personal)
admin.site.register(Machine)
admin.site.register(Material)
admin.site.register(MaterialType)
admin.site.register(MaterialPerObekt)
admin.site.register(OrderMachine)
admin.site.register(OrderMaterial)
admin.site.register(OrderMat)
admin.site.register(OrderMaterialPerObekt)

