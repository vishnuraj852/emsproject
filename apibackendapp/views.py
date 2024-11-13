from django.shortcuts import render
from .models import Department, Employee
from rest_framework import viewsets , filters
from .serializers import EmployeeSerializer, DepartmentSerializer, UserSerializer, SignupSerializer ,  LoginSerializers
from django.contrib.auth.models import User
from rest_framework.permissions import IsAuthenticated , AllowAny
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate
# Create your views here.

class SignupAPIView(APIView):
    permission_classes = [AllowAny]
    def post(self,request):
        serializers = SignupSerializer(data = request.data)
        if serializers.is_valid():
            user = serializers.save()
            token, created = Token.objects.get_or_create(user = user)
            return Response({
                "user_id":user.id,
                "username": user.username,
                "token": token.key,
                "role": user.groups.all()[0].id if user.groups.exists() else None

            }, status=status.HTTP_201_CREATED)
        else:
            response = {'status':status.HTTP_400_BAD_REQUEST,'data':serializers.errors}
            return Response(response, status= status.HTTP_400_BAD_REQUEST)

class LoginAPIView(APIView):
    permission_classes = [AllowAny]
    def post(self,request):
        serializers = LoginSerializers(data = request.data)
        if serializers.is_valid():
            username = serializers.validated_data['username']
            password = serializers.validated_data['password']
            user = authenticate(request, username=username,password=password)
            if user is not None:
                token = Token.objects.get(user=user)
                response = {
                    "status": status.HTTP_200_OK,
                    "message":"sucess",
                    "username":user.username,
                     "role": user.groups.all()[0].id if user.groups.exists() else None,
                     "data":{
                         "Token": token.key
                     }

                }
                return Response(response, status=status.HTTP_200_OK)
            else:
                response = {
                    "status": status.HTTP_401_UNAUTHORIZED,
                    "message": "Invalid username or password",
                }
            return Response(response, status=status.HTTP_401_UNAUTHORIZED)
        else:
            response = {'status':status.HTTP_400_BAD_REQUEST,'data':serializers.errors}
            return Response(response, status= status.HTTP_400_BAD_REQUEST)



class DepartmentViewSet(viewsets.ModelViewSet):
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer  # Corrected here
    permission_classes =[IsAuthenticated]

class EmployeeViewSet(viewsets.ModelViewSet):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer  # Corrected here
    filter_backends = [filters.SearchFilter]
    search_fields = ['employee_name','designation']
    permission_classes =[]

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer  # Corrected here
    permission_classes =[IsAuthenticated]