# imports
import json
from random import randint

from django.contrib.auth import authenticate, get_user_model
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.tokens import RefreshToken

from .models import Profile
from .serializers import (LoginSerializer, ProfileSerializer,
                          RegisterSerializer, VerifyUserSerializer)

# User
User = get_user_model()

# JWT Generator.
def jwt_generator(user):
 refresh = RefreshToken.for_user(user)
 return {
  'refresh': str(refresh),
  'access': str(refresh.access_token),
 }


# Register new user view
class RegisterUser(APIView):
 def post(self,request):
  sr = RegisterSerializer(data=request.data)
  if sr.is_valid(raise_exception=True):
   sr.save()
   return Response({'msg':'user created'},status=status.HTTP_201_CREATED)
  
  return Response({'errors':'user not created'},status=status.HTTP_400_BAD_REQUEST)

# Verify User
class VerifyUser(APIView):
  authentication_classes = [JWTAuthentication]
  permission_classes = [IsAuthenticated]

  def post(self, request):
    sr = VerifyUserSerializer(data=request.data)
    sr.is_valid(raise_exception=True)
    user = Profile.objects.get(user=request.user)
    serverCode = user.verifying_code
    userCode = sr.data.get('user_code')
    if serverCode == userCode:
      user.verified = True
      user.save()
      return Response({'msg':'Verified Successfully'},status=status.HTTP_202_ACCEPTED)
    else:
      return Response({'errors':'Verify code is not valid'},status=status.HTTP_400_BAD_REQUEST)

# login view:
# Authenticate User and give a response
class LoginView(APIView):
 def post(self,request):
  sr = LoginSerializer(data=request.data)
  sr.is_valid(raise_exception=True)
  email = sr.data.get('email')
  password = sr.data.get('password')
  user = authenticate(email=email,password=password)
  
  if user is not None:
   token = jwt_generator(user)
   profile = Profile.objects.get(user=user)
 
   auth = {
    'email':user.email,
    'name':profile.name,
    'image':profile.img.url,
    'verified':profile.verified
   }
   return Response({
    'token':token,
    'auth':auth,
    'msg':'login success'
    },
    status=status.HTTP_201_CREATED
   )
  else:
   return Response({'errors':{'non_field_errors':['Email or Password is not Valid']}}, status=status.HTTP_404_NOT_FOUND)



