from rest_framework.permissions import IsAuthenticated,AllowAny
from rest_framework.response import Response
from rest_framework.generics import RetrieveAPIView,ListAPIView
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.decorators import api_view
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken

from app1.api.v1.serializers.app1serializers import *
from app1.models import *


class RegisterView(APIView):
    permission_classes=[AllowAny]
    
    def post(self,request):
        serializer=UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message':'successfully registered'},status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    permission_classes = [AllowAny]
    
    def post(self, request,*args,**kwargs):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            return Response(data=serializer.validated_data,status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DoctorView(ListAPIView):
    permission_class=[IsAuthenticated]
    serializer_class=GetUserSerializer
    queryset=User.objects.all
    
    def get_queryset(self):
        user=self.request.user
        qs = super().get_queryset()     
        id=self.kwargs['id']
        if user.is_doctor==True:
            if id==None: 
                qs = super().get_queryset() 
                return qs.filter(is_doctor=True)
            else:
                qs = super().get_queryset() 
                return qs.filter(id=self.kwargs['id'])

        return Response({'message':'you are not a doctor'},status=status.HTTP_400_BAD_REQUEST)
            
            


    

        
    