from django.contrib import admin
from django.db.models import Q
from django import forms
from django.core.files.storage import default_storage
from django.conf import settings
import os

from .models import Category, Wishlistproducts, Wishlist, User, Referal, Propertyname, Property, Product, Media, ProductProperties
from .tasks import send_media_task
from settings.settings import config


class MediaForm(forms.ModelForm):
    unput_media = forms.FileField(required=True)

    class Meta:
        model = Media
        fields = "__all__"
    
    def save(self, commit = True):
        obj = super().save(commit=False)
        print("dadssf")
        uploaded_file = self.cleaned_data["unput_media"]
        path = os.path.join(settings.MEDIA_ROOT,"uploads",uploaded_file.name)
        obj.save()
        send_media_task.delay(config.tg_bot.token,path,obj.media_id,config.tg_bot.channel_id)
        return obj
    

class MediaInline(admin.StackedInline):
    model = Media
    form = MediaForm
    extra = 0
    

class MediaAdmin(admin.ModelAdmin):
    form = MediaForm

   
        


class ProductPropertiesInline(admin.StackedInline):
    model = ProductProperties
    raw_id_fields = ["property"]
    extra = 0


class PropertyInline(admin.StackedInline):
    model = Product.properties.through
    extra = 0


class ProductAdmin(admin.ModelAdmin):
    inlines = [ProductPropertiesInline, MediaInline]
    search_fields = ["title"]
    list_filter = ["title", "price", "category__name", "properties"]
    raw_id_fields = ["properties", "category"]


admin.site.register(Product, ProductAdmin)


class PropertyAdmin(admin.ModelAdmin):
    inlines = [ProductPropertiesInline]
    search_fields = ["property__name", "description"]
    raw_id_fields = ("property",)

    def get_search_results(self, request, queryset, search_term):
        queryset, may_have_duplicates = super().get_search_results(
            request, queryset, search_term)

        if ":" in search_term:
            name, description = search_term.split(":", 1)

            queryset |= self.model.objects.filter(
                Q(property__name=name.strip()) & Q(description=description.strip()))
        else:
            queryset |= self.model.objects.filter(
                Q(property__name=search_term) & Q(description=search_term))
        return queryset, may_have_duplicates


class CategoryAdmin(admin.ModelAdmin):
    search_fields = ["name"]
    list_filter = ["name"]

    # мейби сделать поиск по подкатегориям типа имя родительской -> все ее дети


admin.site.register(Property, PropertyAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Wishlistproducts)
admin.site.register(Wishlist)
admin.site.register(User)
admin.site.register(Referal)
admin.site.register(Propertyname)
# Register your models here.
