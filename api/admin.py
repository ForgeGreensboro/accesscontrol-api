from django.contrib import admin

from . import models
# Register your models here.

@admin.register(models.Machine)
class MachineAdmin(admin.ModelAdmin):
    pass

@admin.register(models.Member)
class MemberAdmin(admin.ModelAdmin):
    pass

@admin.register(models.SignOff)
class SignOffAdmin(admin.ModelAdmin):
    pass

@admin.register(models.Shop)
class ShopAdmin(admin.ModelAdmin):
    pass

@admin.register(models.Reservation)
class ReservationAdmin(admin.ModelAdmin):
    pass
