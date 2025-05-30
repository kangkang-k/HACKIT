from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import CustomUser

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']

    def update(self, instance, validated_data):
        instance.username = validated_data.get('username', instance.username)
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.email = validated_data.get('email', instance.email)
        instance.save()
        return instance


class UserSerializer2(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['phone_number', 'birth_date', 'completed_tasks', 'bio', 'code_age']


class BalanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['balance']
