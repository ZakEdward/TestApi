from rest_framework import serializers
from .models import User



class PhoneNumberSerializer(serializers.Serializer):
    phone_number = serializers.CharField(max_length=15)


class VerificationCodeSerializer(serializers.Serializer):
    phone_number = serializers.CharField(max_length=15)
    code = serializers.CharField(max_length=4)


class UserProfileSerializer(serializers.ModelSerializer):
    referred_users = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['phone_number', 'invite_code', 'referred_by', 'referred_users', 'is_verified']

    def get_referred_users(self, obj):
        return User.objects.filter(referred_by=obj).values_list('phone_number', flat=True)
