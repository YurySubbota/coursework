from django.contrib import admin

from equipmentrental.models import Equipment, Photo


class PhotoInline(admin.StackedInline):
    model = Photo


@admin.register(Equipment)
class EquipmentAdmin(admin.ModelAdmin):
    list_display = ('id', 'category', 'manufacturer', 'model')
    search_fields = ('id', 'category', 'manufacturer', 'model')
    list_filter = ('category', 'manufacturer', 'model')
    inlines = (PhotoInline,)
