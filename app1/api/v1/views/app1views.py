from rest_framework.permissions import IsAuthenticated,AllowAny
from rest_framework.response import Response
from rest_framework.generics import RetrieveAPIView,ListAPIView
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.decorators import api_view,permission_classes
from rest_framework import permissions
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
    
    def get_queryset(self):
        user=self.request.user
        if user.usertype=='Doctor': 
            data = User.objects.filter(usertype='Doctor')
            return data
        return Response({'message':'you are not a doctor'},status=status.HTTP_400_BAD_REQUEST)
 
            
@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes(( permissions.IsAuthenticated,))
def doctor_profile_view(request,pk):
    
    try:
        user=User.objects.get(id=pk)
    except user.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    currentuser=request.user
    if currentuser.id == user.pk:

        if request.method == 'GET':
            serializer = UserProfileSerializer(user)
            return Response(serializer.data)

        elif request.method == 'PUT':
            serializer = UserProfileSerializer(user, data=request.data,partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        elif request.method == 'DELETE':
            user.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
    else:
        return Response({'message': 'Invalid id'},status=status.HTTP_400_BAD_REQUEST)


class PatientView(ListAPIView):
    permission_class=[IsAuthenticated]
    serializer_class=GetUserSerializer
    
    def get_queryset(self):
        user=self.request.user
        if user.usertype=='Doctor': 
            data = User.objects.filter(usertype='Patient')
            return data
        return Response({'message':'you are not a doctor'},status=status.HTTP_400_BAD_REQUEST)
 
 
@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes((permissions.IsAuthenticated,))
def patient_profile_view(request,pk):
    
    try:
        user=User.objects.get(id=pk)
    except user.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    currentuser=request.user
    if (currentuser.id == user.pk or currentuser.usertype=='Doctor') and user.usertype=='Patient':

        if request.method == 'GET':
            serializer = UserProfileSerializer(user,many=True)
            return Response(serializer.data)

        elif request.method == 'PUT':
            serializer = UserProfileSerializer(user, data=request.data,partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        elif request.method == 'DELETE':
            user.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
    else:
        return Response({'message': 'Invalid user'},status=status.HTTP_400_BAD_REQUEST)


class PatientRecordView(ListAPIView):
    permission_class = [IsAuthenticated]
    queryset = Patient_Records.objects.all()
    serializer_class = PatientRecordSerializer
    
    def post(self,request):
        user=self.request.user
        request.data._mutable=True
        data=request.data
        data['departments']=user.departments.id
        serializer=PatientRecordSerializer(data=request.data)
        if user.usertype=='Doctor':
            if serializer.is_valid():
                serializer.save()
                return Response("patient record added successfully")
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
        return Response({'message':'you are not a doctor'},status=status.HTTP_400_BAD_REQUEST)
    
    def get_queryset(self):
        user=self.request.user
        serializer=GetPatientRecordSerializer
        if user.usertype=='Doctor':
            data=Patient_Records.objects.all()
            return data 
        return Response({'message':'invalid request'},status=status.HTTP_400_BAD_REQUEST)
  
        
@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes((permissions.IsAuthenticated,))
def patient_record_view(request,pk):
    try:
        user=User.objects.get(id=pk)
    except user.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    currentuser=request.user
    
    if currentuser.id == user.pk or currentuser.usertype == 'Doctor':
        patient_record = Patient_Records.objects.get(pk=pk)

        if request.method == 'GET':
            serializer = PatientRecordSerializer(patient_record)
            return Response(serializer.data)

        elif request.method == 'PUT':
            serializer = PatientRecordSerializer(patient_record, data=request.data,Partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        elif request.method == 'DELETE':
            patient_record.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
    else:
        return Response({'message': 'Invalid user'},status=status.HTTP_400_BAD_REQUEST)
    
    
class DepartmentView(ListAPIView):
    permission_class = [IsAuthenticated]
    queryset = Departments.objects.all()
    serializer_class = DepartmentSerializer
   
    def get_queryset(self):
        user = self.request.user
        return Departments.objects.all()

    def post(self, request):
        data=request.data      
        serializer = DepartmentSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Department created successfully'}, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        

@api_view(['GET','PUT',])
@permission_classes((permissions.IsAuthenticated,))
def department_doctor_view(request,pk):
    try:
        user=User.objects.filter(usertype='Doctor',departments__pk=pk)
    except user.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    currentuser=request.user
    
    if currentuser.departments.id==pk and currentuser.usertype=='Doctor':
        if request.method=='GET':
            serializer = UserProfileSerializer(user,many=True)
            print(user)
            return  Response (serializer.data)
        
@api_view(['GET','PUT',])
@permission_classes((permissions.IsAuthenticated,))
def department_patient_view(request,pk):
    try:
        user=User.objects.filter(usertype='Patient',departments__pk=pk)
    except user.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    currentuser=request.user
    
    if currentuser.departments.id==pk and currentuser.usertype=='Doctor':
        if request.method=='GET':
            serializer = UserProfileSerializer(user,many=True)
            print(user)
            return  Response (serializer.data)
        
        
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def user_logout(request):
    if request.method == 'POST':
        try:
            # Delete the user's token to logout
            request.auth=""
            return Response({'message': 'Successfully logged out.'}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
        
    
    
    
                  

