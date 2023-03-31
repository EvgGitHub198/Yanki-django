from rest_framework import serializers
from .models import Product, Category
from django.core.files.base import ContentFile


class ProductSerializer(serializers.ModelSerializer):
    image = serializers.ImageField()
    category = serializers.SlugRelatedField(
        queryset=Category.objects.all(),
        slug_field='slug'
    )

    class Meta:
        model = Product
        fields = (
            'id',
            'name',
            'slug',
            'get_absolute_url',
            'description',
            'price',
            'category',
            'image'
        )
        read_only_fields = ('id', 'get_absolute_url')

    def create(self, validated_data):
        category_name = validated_data.pop('category')
        category, created = Category.objects.get_or_create(name=category_name)
        validated_data['category'] = category
        image = validated_data.pop('image', None)
        instance = super().create(validated_data)
        if image:
            instance.image.save(image.name, ContentFile(image.read()))

        return instance





class CategorySerializer(serializers.ModelSerializer):
    products = ProductSerializer(many=True, required=False)
    class Meta:
        model = Category
        fields = (
            'id',
            'name',
            'slug',
            'get_absolute_url',
            'products',
        )
