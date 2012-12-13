from django.contrib import admin
from myfruitcake.models import Fruitcake, Shipment

### Admin

class FruitcakeAdmin(admin.ModelAdmin):
    list_display = ['id','dt', 'uploader', 'popup', 'pic']
    search_fields = ['id','dt','uploader','popup', 'pic']
    exclude = ('shipments', 'uploads')
    list_filter = ['dt', 'uploader']
    date_hierarchy = 'dt'

class UploadAdmin(admin.ModelAdmin):
    pass

"""
class EmailContactInline(admin.TabularInline):
    model = EmailContact
    extra = 3

admin.site.register(EmailContact)
"""

class ShipmentAdmin(admin.ModelAdmin):
    list_display = ['dt', 'fruitcake', 'sender', 'message']
    search_fields = ['message']
#    inlines = [EmailContactInline]
    list_filter = ['dt']
    date_hierarchy = 'dt'

admin.site.register(Fruitcake, FruitcakeAdmin)
admin.site.register(Shipment, ShipmentAdmin)

