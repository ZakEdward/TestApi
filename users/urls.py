from django.urls import path
from .views import PhoneNumberView, VerificationCodeView, UserProfileView


urlpatterns = [
    path('auth/phone/', PhoneNumberView.as_view(), name='phone-number'),
    path('auth/verify/', VerificationCodeView.as_view(), name='verification-code'),
    path('profile/<int:user_id>/', UserProfileView.as_view(), name='user-profile'),

]