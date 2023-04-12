from djoser.serializers import UserCreateSerializer
from django.contrib.auth import get_user_model, login
from rest_framework import serializers

User = get_user_model()

class CustomUserCreateSerializer(UserCreateSerializer):

    class Meta(UserCreateSerializer.Meta):
        model = User
        fields = ('email', 'username', 'password')

    def validate(self, attrs):
        if User.objects.filter(email=attrs['email']).exists():
            raise serializers.ValidationError('This email has already been used.')
        return attrs
    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        login(self.context['request'], user)
        return user