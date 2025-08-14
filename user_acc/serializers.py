from rest_framework.authtoken.models import Token
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework import status
from .models import CustomUser

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['username', 'first_name', 'last_name', 'address', 'age']


class RegisterSerializers(serializers.ModelSerializer):
    password = serializers.CharField(max_length=15, write_only=True)
    confirm_password = serializers.CharField(max_length=15, write_only=True)

    class Meta:
        model = CustomUser
        fields = ['username', 'first_name', 'last_name', 'address', 'age', 'password', 'confirm_password']

    def validate(self, data):
        if data['password'] != data['confirm_password']:
            raise ValidationError({'status':status.HTTP_400_BAD_REQUEST, 'message':'parollar mos emas'})
        username = data['username']
        if CustomUser.objects.filter(username=username).exists():
            raise ValidationError({'error': 'This username already taken', 'status':status.HTTP_400_BAD_REQUEST})
        return data

    def create(self, validated_data):
        validated_data.pop('confirm_password')
        user = CustomUser.objects.create(
            username = validated_data['username'],
            first_name = validated_data['first_name'],
            last_name = validated_data['last_name'],
            age = validated_data['age'],
            address = validated_data['address']
        )
        user.set_password(validated_data['password'])
        user.save()
        Token.objects.create(user=user)
        return user