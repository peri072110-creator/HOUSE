from django.contrib import admin
from modeltranslation.admin import TranslationAdmin

from .models import (
    UserProfile,
    Region,
    City,
    District,
    Property,
    PropertyImage,
    PropertyDocument,
    Review
)


class PropertyImageInline(admin.TabularInline):
    model = PropertyImage
    extra = 1

class PropertyDocumentInline(admin.TabularInline):
    model = PropertyDocument
    extra = 1


@admin.register(Property)
class PropertyAdmin(TranslationAdmin):
    inlines = [PropertyImageInline, PropertyDocumentInline]

    class Media:
        js = (
            'http://ajax.googleapis.com/ajax/libs/jquery/1.9.1/jquery.min.js',
            'http://ajax.googleapis.com/ajax/libs/jqueryui/1.10.2/jquery-ui.min.js',
            'modeltranslation/js/tabbed_translation_fields.js',
        )
        css = {
            'screen': ('modeltranslation/css/tabbed_translation_fields.css',),
        }


admin.site.register(UserProfile)
admin.site.register(Region)
admin.site.register(City)
admin.site.register(District)
admin.site.register(Review)
