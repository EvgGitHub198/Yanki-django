from rest_framework import serializers
from .models import Product, Category, ProductSize, Size, ExtraImage
from django.core.files.base import ContentFile
from django.db import transaction

class SizeSerializer(serializers.Serializer):
    name = serializers.ChoiceField(choices=['XS', 'S', 'M', 'L', 'XL', 'XXL'])




class ExtraImageSerializer(serializers.ModelSerializer):
    image = serializers.ImageField()

    class Meta:
        model = ExtraImage
        fields = ('id', 'image')


class ProductSizeSerializer(serializers.ModelSerializer):
    size = serializers.CharField(source='size.name')
    quantity = serializers.IntegerField()

    class Meta:
        model = ProductSize
        fields = ('size', 'quantity')

    def to_internal_value(self, data):
        size_data = {
            'size': data['size'],
            'quantity': data['quantity']
        }
        return size_data

    

class ProductSerializer(serializers.ModelSerializer):
    main_image = serializers.ImageField(required=False)
    category = serializers.SlugRelatedField(
        queryset=Category.objects.all(),
        slug_field='slug'
    )
    extra_images = ExtraImageSerializer(many=True, required=False)
    sizes = ProductSizeSerializer(many=True, source='size_quantities')

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

    def create(self, validated_data):

        sizes_data = validated_data.pop('size_quantities', [])
        category_name = validated_data.pop('category')
        category, created = Category.objects.get_or_create(name=category_name)
        validated_data['category'] = category
        main_image = validated_data.pop('main_image', None)
        extra_images_data = validated_data.pop('extra_images', [])


        product = Product.objects.create(**validated_data)
        for size_data in sizes_data:
            size_name = size_data['size']
            size_queryset = Size.objects.filter(name=size_name)
            if size_queryset.exists():
                size = size_queryset.first()
            else:
                size = Size.objects.create(name=size_name)
            quantity = size_data['quantity']
            product.size_quantities.create(size=size, quantity=quantity)


        if main_image:
            product.main_image.save(main_image.name, ContentFile(main_image.read()))

        for extra_image_data in extra_images_data:
            extra_image = ExtraImage.objects.create(image=extra_image_data['image'])
            product.extra_images.add(extra_image)


        return product



    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.description = validated_data.get('description', instance.description)
        instance.price = validated_data.get('price', instance.price)
        instance.sale = validated_data.get('sale', instance.sale)
        instance.slug = validated_data.get('slug', instance.slug)

        # обновление категории
        category_name = validated_data.get('category', instance.category.name)
        category, created = Category.objects.get_or_create(name=category_name)
        instance.category = category

        # обновление главного изображения
        main_image = validated_data.get('main_image')
        if main_image:
            instance.main_image.save(main_image.name, ContentFile(main_image.read()))

        # обновление дополнительных изображений
        extra_images_data = validated_data.get('extra_images')
        if extra_images_data:
            # удаляем старые дополнительные изображения
            instance.extra_images.all().delete()

            # создаем новые дополнительные изображения
            for extra_image_data in extra_images_data:
                extra_image = ExtraImage.objects.create(image=extra_image_data['image'])
                instance.extra_images.add(extra_image)

        # обновление размеров
        sizes_data = validated_data.pop('size_quantities', [])

        if sizes_data:
            # удаляем старые размеры
            instance.size_quantities.all().delete()

            # создаем новые размеры
            for size_data in sizes_data:
                
                size_name = size_data['size']
                size_queryset = Size.objects.filter(name=size_name)
                if size_queryset.exists():
                    size = size_queryset.first()
                else:
                    size = Size.objects.create(name=size_name)
                quantity = size_data['quantity']
                instance.size_quantities.create(size=size, quantity=quantity)

        instance.save()
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
