from django.contrib import admin
from .models import Address, AddressCode, Deal, Location


class AddressAdmin(admin.ModelAdmin):
    list_display = ("sido_code", "gugun_code", "dong_code")


admin.site.register(Address, AddressAdmin)


class AddressCodeAdmin(admin.ModelAdmin):
    list_display = ("code", "name", "gubun")
    list_filter = ("gubun", )


admin.site.register(AddressCode, AddressCodeAdmin)


class DealAdmin(admin.ModelAdmin):
    list_display = ("bldg_nm", "bldg_area", "sum_amount", "dong", "bobn", "deal_dd")
    raw_id_fields = ("location",)
    search_fields = ["bldg_nm", "dong"]


admin.site.register(Deal, DealAdmin)


class DealInline(admin.TabularInline):
    model = Deal


class LocationAdmin(admin.ModelAdmin):

    list_display = ("title", "buildingAddress", "localName_1")
    inlines = [DealInline]
    search_fields = ["title", "bldg_nm"]


admin.site.register(Location, LocationAdmin)
