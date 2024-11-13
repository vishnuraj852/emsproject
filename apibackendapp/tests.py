from django.test import TestCase
from rest_framework.test import APITestCase, APIClient
from .models import Department ,Employee
from datetime import date
from django.urls import reverse
from .serializers import EmployeeSerializer

from rest_framework import status
# Create your tests here.
class EmployeeViewSetTest(APITestCase):
    def setUp(self):
        self.departments = Department.objects.create(Department_name="HR")
        self.employee = Employee.objects.create(
            employee_name ="jakie",
            designation ="",
            date_of_joining = date(2024,11,13),
            department = self.departments,
            contact ="China",
            is_active = True
        )
        self.client = APIClient()

    def test_employee_details(self):
        url = reverse('employee-detail', args={self.employee.employee_id})
        response = self.client.get(url)
        employees = Employee.objects.all()
        serializer = EmployeeSerializer(self.employee)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)


