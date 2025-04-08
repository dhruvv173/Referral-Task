from rest_framework import serializers
from django.contrib.auth.hashers import make_password
from .models import User

class UserSerializer(serializers.ModelSerializer):
    referral_code = serializers.CharField(required=False)

    class Meta:
        model = User
        fields = ['id', 'email', 'name', 'mobile_number', 'city', 'referral_code', 'password']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
            referral_code = validated_data.pop('referral_code', None)
            referred_by = None

            if referral_code:
                try:
                    referred_by = User.objects.get(referral_code=referral_code)
                except User.DoesNotExist:
                    raise serializers.ValidationError("Invalid referral code")
            validated_data['password'] = make_password(validated_data['password'])        
            user = User.objects.create(
                referred_by=referred_by,
                **validated_data
            )
            user.referral_code = user.generate_referral_code()
            user.save()
            return user    
        
class ReferralSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['name', 'email', 'created_at']