from rest_framework import serializers
from .models import Product, Category, ProductSize, Size, ExtraImage
from django.core.files.base import ContentFile


class SizeSerializer(serializers.Serializer):
    name = serializers.ChoiceField(choices=['XS', 'S', 'M', 'L', 'XL', 'XXL'])

    def to_representation(self, obj):
        return obj.name

    def to_internal_value(self, data):
        return {'name': data}



class ExtraImageSerializer(serializers.ModelSerializer):
    image = serializers.ImageField()

    class Meta:
        model = ExtraImage
        fields = ('id', 'image')





class ProductSerializer(serializers.ModelSerializer):
    main_image = serializers.ImageField()
    category = serializers.SlugRelatedField(
        queryset=Category.objects.all(),
        slug_field='slug'
    )
    extra_images = ExtraImageSerializer(many=True)
    sizes = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = (
            'id',
            'name',
            'slug',
            'get_absolute_url',
            'description',
            'price',
            'sale',
            'category',
            'main_image',
            'extra_images',
            'sizes',
        )
        read_only_fields = ('id', 'get_absolute_url')
  

    def get_sizes(self, obj):
        sizes = []
        product_sizes = ProductSize.objects.filter(product=obj)
        for product_size in product_sizes:
            size = product_size.size
            quantity = product_size.quantity
            sizes.append({
                'size': size,
                'quantity': quantity,
            })
        return sizes


    def create(self, validated_data):
        sizes_data = validated_data.pop('sizes')
        category_name = validated_data.pop('category')
        category, created = Category.objects.get_or_create(name=category_name)
        validated_data['category'] = category
        main_image = validated_data.pop('main_image', None)
        extra_images_data = validated_data.pop('extra_images', [])

        instance = super().create(validated_data)
        if main_image:
            instance.main_image.save(main_image.name, ContentFile(main_image.read()))

        for size_data in sizes_data:
            size, created = Size.objects.get_or_create(**size_data['size'])
            ProductSize.objects.create(product=instance, size=size, quantity=size_data['quantity'])

        for extra_image_data in extra_images_data:
            extra_image = ExtraImage.objects.create(image=extra_image_data['image'])
            instance.extra_images.add(extra_image)

        return instance




class CategorySerializer(serializers.ModelSerializer):
    products = ProductSerializer(many=True, required=False)
    category_image = serializers.ImageField(required=False)
    class Meta:
        model = Category
        fields = (
            'id',
            'name',
            'slug',
            'get_absolute_url',
            'category_image',
            'products',           
        )
    def create(self, validated_data):   
       category_image = validated_data.pop('category_image', 'None')
       instance = super().create(validated_data)
       if category_image:
           instance.category_image.save(category_image.name, ContentFile(category_image.read()))


       return instance

