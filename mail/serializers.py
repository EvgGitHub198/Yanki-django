from rest_framework import serializers
from django.contrib.auth.models import User
from .models import UserProfile



class UserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(read_only=True)
    phone = serializers.CharField(source='profile.phone')
    index = serializers.CharField(source='profile.index')
    address = serializers.CharField(source='profile.address')
    full_name = serializers.CharField(source='profile.full_name')

    class Meta:
        model = User
        fields = ('email', 'phone', 'index', 'address', 'full_name')

    def create(self, validated_data):
        profile_data = validated_data.pop('profile')
        user = self.context['request'].user  # Получаем текущего пользователя из контекста запроса
        UserProfile.objects.create(user=user, **profile_data)
        return user

    def update(self, instance, validated_data):
        profile_data = validated_data.pop('profile', {})
        profile = instance.profile
        profile.phone = profile_data.get('phone', profile.phone)
        profile.index = profile_data.get('index', profile.index)
        profile.address = profile_data.get('address', profile.address)
        profile.full_name = profile_data.get('full_name', profile.full_name)
        profile.save()

        # Обновляем остальные поля пользователя, если необходимо
        instance.email = validated_data.get('email', instance.email)
        instance.save()

        return instance


