from django.db import models

# Create your models here.

class Category(models.Model):
    category_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=128)
    description = models.CharField(max_length=255, blank=True, null=True)
    parent = models.ForeignKey('self', models.SET_NULL, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'category'
    
    def __str__(self):
        return self.name


MEDIA_TYPES = {
    "video": "Видео",
    "photo": "Фото"
}


class Media(models.Model):
    media_id = models.AutoField(primary_key=True)
    telegram_media_id = models.CharField(unique=True, max_length=255,null=True)
    media_type = models.TextField(choices=MEDIA_TYPES)  # This field type is a guess.
    product = models.ForeignKey('Product', models.CASCADE)
    alt_text = models.CharField(max_length=128, blank=True, null=True)
    is_feature = models.BooleanField()
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'media'
    
    def __str__(self):
        return self.alt_text + ":" + str(self.media_id)


class Product(models.Model):
    product_id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=512)
    description = models.CharField(max_length=1024, blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    available = models.BooleanField()
    properties = models.ManyToManyField(
        "Property", through="ProductProperties")
    category = models.ForeignKey(Category, models.SET_NULL, blank=True, null=True)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'product'
    
    def __str__(self):
        return self.title


class ProductProperties(models.Model):
    product = models.ForeignKey(Product, models.CASCADE)
    property = models.ForeignKey('Property', models.CASCADE)

    class Meta:
        managed = False
        db_table = 'productproperties'
    
    def __str__(self):
        return self.product.title+"->"+str(self.property)


class Property(models.Model):
    description_id = models.AutoField(primary_key=True)
    description = models.CharField(max_length=256)
    property = models.ForeignKey('Propertyname', models.CASCADE)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'property'

    def __str__(self):
        return self.property.name + " : " + self.description


class Propertyname(models.Model):
    property_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=256)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'propertyname'


class Referal(models.Model):
    referrers = models.ForeignKey('User', models.CASCADE)
    refers = models.ForeignKey('User', models.CASCADE, related_name='referal_refers_set')

    class Meta:
        managed = False
        db_table = 'referal'


class User(models.Model):
    user_id = models.BigIntegerField(primary_key=True)
    username = models.CharField(max_length=128, blank=True, null=True)
    full_name = models.CharField(max_length=128)
    email = models.CharField(max_length=128, blank=True, null=True)
    phone = models.CharField(max_length=32, blank=True, null=True)
    active = models.BooleanField()
    wishlist = models.ForeignKey('Wishlist', models.SET_NULL, blank=True, null=True)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'user'


class Wishlist(models.Model):
    wishlist_id = models.AutoField(primary_key=True)

    class Meta:
        managed = False
        db_table = 'wishlist'


class Wishlistproducts(models.Model):
    wishlist = models.ForeignKey(Wishlist, models.CASCADE)
    product = models.ForeignKey(Product, models.CASCADE)

    class Meta:
        managed = False
        db_table = 'wishlistproducts'
