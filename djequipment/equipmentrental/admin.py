from django.contrib import admin

from equipmentrental.models import Equipment, Photo, Booked


class PhotoInline(admin.StackedInline):
    model = Photo


@admin.register(Equipment)
class EquipmentAdmin(admin.ModelAdmin):
    list_display = ('id', 'category', 'manufacturer', 'model', 'status')
    search_fields = ('id', 'category', 'manufacturer', 'model')
    list_filter = ('category', 'manufacturer', 'model')
    inlines = (PhotoInline,)

@admin.register(Booked)
class BookedAdmin(admin.ModelAdmin):
    list_display = ('equipment_id',
                    'phone_number', 'comment')