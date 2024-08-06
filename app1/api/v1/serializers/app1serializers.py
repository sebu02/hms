from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth import authenticate
from django.contrib.auth.models import Group

from app1.models import *

        
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model=User
        fields=['name','username','password','usertype','departments']
    
    def create(self,validated_data):
            username=self.validated_data['username']
            name=self.validated_data['name']
            usertype=self.validated_data['usertype']
            departments=self.validated_data['departments']
            user=User(username=username,name=name,usertype=usertype,departments=departments)
            password = self.validated_data['password']
            user.set_password(password)   
            user.save()
            return user


class GetUserSerializer(serializers.ModelSerializer):
    
    class Meta:
        model=User
        fields=['name']
        
class UserProfileSerializer(serializers.ModelSerializer):
    
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
    

class PatientRecordSerializer(serializers.ModelSerializer):
    
    class Meta:
        model=Patient_Records
        fields=['patient_id','observations','treatments']
    
