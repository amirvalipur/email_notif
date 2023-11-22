from rest_framework import serializers
from .models import CustomUser


class CustomUserSerializer(serializers.ModelSerializer):
    re_password = serializers.CharField(max_length=50, write_only=True)

    class Meta:
        model = CustomUser
        fields = ['email_address', 'name', 'family', 'password', 're_password']
        extra_kwargs = {
            'password': {'write_only': True},
            're_password': {'write_only': True},
        }

    def validate(self, data):
        if data['password'] != data['re_password']:
            raise serializers.ValidationError('رمز عبور و تکرار آن با هم یکی نمی باشد')
        return data


# ___________________________________________________________________________________
class ChangePasswordSerializer(serializers.Serializer):
    password = serializers.CharField(max_length=50, write_only=True)
    re_password = serializers.CharField(max_length=50, write_only=True)

    def validate(self, data):
        if data['password'] != data['re_password']:
            raise serializers.ValidationError('رمز عبور و تکرار آن با هم یکی نمی باشد')
        return data


# ___________________________________________________________________________________

class RememberTokenSerializer(serializers.Serializer):
    password = serializers.CharField(max_length=50, write_only=True)
    email_address = serializers.EmailField()
