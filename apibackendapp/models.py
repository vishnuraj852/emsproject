from django.db import models
from django.db.models.signals import post_save
# Create your models here.
from django.dispatch import receiver
from django.conf import settings
from rest_framework.authtoken.models import Token

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created =False,**kwargs):
    if created:
        Token.objects.create(user=instance)




#models here


class Department(models.Model):
    Department_id = models.AutoField(primary_key=True)
    Department_name = models.CharField(max_length=200)

def __str__(self):
    return self.Department_name



class Employee(models.Model):
    employee_id = models.AutoField(primary_key=True)
    employee_name = models.CharField(max_length=200)
    designation = models.CharField(max_length=150)
    date_of_joining = models.DateField()
    department = models.ForeignKey('Department', on_delete=models.CASCADE)  # Department model should be defined
    contact = models.CharField(max_length=150)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.employee_name
