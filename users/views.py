from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import User
from .serializers import PhoneNumberSerializer, VerificationCodeSerializer, UserProfileSerializer
import random
import string
import time
import logging

logger = logging.getLogger(__name__)

class PhoneNumberView(APIView):
    def post(self, request):
        serializer = PhoneNumberSerializer(data=request.data)
        if serializer.is_valid():
            phone_number = serializer.validated_data['phone_number']
            # Имитация отправки кода
            code = ''.join(random.choices('0123456789', k=4))
            time.sleep(random.uniform(1, 2))
            # Сохранение кода в базе данных
            user, created = User.objects.get_or_create(phone_number=phone_number)
            user.verification_code = code
            user.save()
            return Response({'message': 'Code sent', 'code':code}, status=status.HTTP_200_OK)
        else:
            logger.error(f'Validation error: {serializer.errors}')
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class VerificationCodeView(APIView):
    def post(self, request):
        serializer = VerificationCodeSerializer(data=request.data)
        if serializer.is_valid():
            phone_number = serializer.validated_data['phone_number']
            code = serializer.validated_data['code']
            try:
                user = User.objects.get(phone_number=phone_number)
                if user.verification_code == code:
                    user.is_verified = True
                    user.verification_code = None  # Сбросить код после успешной верификации
                    user.save()
                    return Response({'message': 'User authenticated', 'user_id': user.id}, status=status.HTTP_200_OK)
                else:
                    return Response({'message': 'Invalid code'}, status=status.HTTP_400_BAD_REQUEST)
            except User.DoesNotExist:
                return Response({'message': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
        else:
            logger.error(f'Validation error: {serializer.errors}')
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserProfileView(APIView):
    def get(self, request, user_id):
        try:
            user = User.objects.get(id=user_id)
            serializer = UserProfileSerializer(user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response({'message': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

    def post(self, request, user_id):
        try:
            user = User.objects.get(id=user_id)
            invite_code = request.data.get('invite_code')
            if invite_code:
                try:
                    referred_by_user = User.objects.get(invite_code=invite_code)
                    if not user.referred_by:
                        user.referred_by = referred_by_user
                        user.save()
                        return Response({'message': 'Invite code activated'}, status=status.HTTP_200_OK)
                    else:
                        return Response({'message': 'Invite code already activated'}, status=status.HTTP_400_BAD_REQUEST)
                except User.DoesNotExist:
                    return Response({'message': 'Invalid invite code'}, status=status.HTTP_400_BAD_REQUEST)
            return Response({'message': 'No invite code provided'}, status=status.HTTP_400_BAD_REQUEST)
        except User.DoesNotExist:
            return Response({'message': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
