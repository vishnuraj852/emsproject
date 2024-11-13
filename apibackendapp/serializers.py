from rest_framework import serializers
from .models import Employee ,Department
from django.contrib.auth.models import User, Group
from django.contrib.auth.hashers import make_password

class SignupSerializer(serializers.ModelSerializer):
    group_name = serializers.CharField(write_only=True, required=False)
    def create(self, validated_data):
        group_name = validated_data.pop("group_name", None)
        validated_data['password'] = make_password(validated_data.get("password"))
        #create the user
        user = super(SignupSerializer, self).create(validated_data)
        if group_name:
            group, created =Group.objects.get_or_create(name=group_name)
            user.groups.add(group)
        return user
    class Meta:
        model = User
        fields = ['username','password','group_name']

class LoginSerializers(serializers.ModelSerializer):
    username = serializers.CharField()
    class Meta:
        model = User
        fields = ['username','password']

class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields =('Department_id','Department_name')
       

#add employee name validation
def name_validation(employee_name):
    if len(employee_name) < 3:
        raise serializers.ValidationError("Name must be atleast 3 chars")
    return employee_name




class EmployeeSerializer(serializers.ModelSerializer):
    Department = DepartmentSerializer(source ='department',read_only=True)
    #adding validation
    employee_name = serializers.CharField(max_length=200, validators=[name_validation])
    class Meta:
        model = Employee
        fields =('employee_id','employee_name','designation','date_of_joining','contact','is_active','department_id','Department')

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields =('id','username')


