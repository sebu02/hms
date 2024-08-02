from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth import authenticate
from django.contrib.auth.models import Group

from app1.models import *

        
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model=User
        fields=['name','username','password','is_doctor',]
    
    def save(self):
            user = User(username=self.validated_data['username'], name=self.validated_data['name'],
                        is_doctor=self.validated_data['is_doctor'])
            password = self.validated_data['password']
            user.set_password(password)
            user.save()
            return user


class GetUserSerializer(serializers.ModelSerializer):
    
    class Meta:
        model=User
        fields='__all__'
    

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()
    
    def validate(self, attrs):
        validated_data = super().validate(attrs)
        if not User.objects.filter(username=validated_data['username']).exists():
            raise serializers.ValidationError('username does not exists')
        user = User.objects.get(username=validated_data['username'])

        creds = {
            'username': user.username,
            'password': validated_data['password']
        }
        
        user = None
        data = {}
        user = authenticate(**creds)
        
        if not user:
            raise serializers.ValidationError('Invalid credentials')
            
        refresh = TokenObtainPairSerializer.get_token(user)

        data["refresh"] = str(refresh)
        data["access"] = str(refresh.access_token)
        return data
    
