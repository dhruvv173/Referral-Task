from django.contrib.auth.hashers import check_password
from rest_framework.views import APIView
from .models import User
from rest_framework import status
from rest_framework.response import Response
from .serializers import UserSerializer, ReferralSerializer


class RegisterView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message":"User Registered successfully"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class LoginView(APIView):
    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response({"error":"User not found"})
        
        if check_password(password, user.password):
            return Response({"message":"Login Successful"})
        return Response({"error": "Invalid credentials, Please check your email/password and try again!"}, status=status.HTTP_401_UNAUTHORIZED)
    
class ReferralView(APIView):
    def get(self, request):
        email = request.query_params.get('email')

        if not email:
            return Response({"error":"Email cannot be blank"})
        
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response({"error":"User not found"})
        
        referees = User.objects.filter(referred_by=user)
        serializer = ReferralSerializer(referees, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    

