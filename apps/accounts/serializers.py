# imports
from dataclasses import fields

from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.core.mail import send_mail
from django.utils.encoding import (DjangoUnicodeDecodeError, force_bytes,
                                   smart_str)
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from .models import Profile

# User
User = get_user_model()

# Register a User:
class RegisterSerializer(serializers.ModelSerializer):

 email = serializers.EmailField(required=True,
  validators=[UniqueValidator(queryset=User.objects.all())]
 )
 password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
 confirm_password = serializers.CharField(write_only=True, required=True)

 class Meta:
  model = User
  fields = ('password', 'confirm_password','email', 'first_name', 'last_name')
  extra_kwargs = {
   'first_name': {'required': True},
   'last_name': {'required': True}
  }

 def validate(self, attrs):
  if attrs['password'] != attrs['confirm_password']:
   raise serializers.ValidationError({"password": "Password didn't match."})
  return attrs

 def create(self, validated_data):
  user = User.object.create(
    email=validated_data['email'],
    first_name=validated_data['first_name'],
    last_name=validated_data['last_name']
   )
  user.set_password(validated_data['password'])
  user.save()
  return user

# login Serializer
class LoginSerializer(serializers.ModelSerializer):
 email = serializers.EmailField(max_length=255)
 class Meta:
  model = User
  fields = ['email', 'password']

# Profile Serializer
class ProfileSerializer(serializers.ModelSerializer):
  class Meta:
    model = Profile
    fields = ['name','gender','img','bio', 'verified']
