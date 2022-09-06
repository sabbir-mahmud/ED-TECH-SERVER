# imports
import json

from django.contrib.auth import authenticate
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.tokens import RefreshToken

from .models import Profile
from .serializers import LoginSerializer, ProfileSerializer, RegisterSerializer


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
   return Response({},status=status.HTTP_201_CREATED)
  
  return Response({},status=status.HTTP_400_CREATED)

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



