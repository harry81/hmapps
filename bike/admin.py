from django.contrib import admin
from .models import Center, StateCenter


class CenterAdmin(admin.ModelAdmin):
    list_display = ("station_name", "station_id")


admin.site.register(Center, CenterAdmin)


class StateCenterAdmin(admin.ModelAdmin):
    list_display = ("center", "parking_bike_tot_cnt", "rack_tot_cnt", "created")
    readonly_fields = ('center',)
    search_fields = ('center__station_name', )


admin.site.register(StateCenter, StateCenterAdmin)
