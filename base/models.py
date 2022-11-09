from django.db import models
from django.utils.translation import gettext_lazy
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from phonenumber_field.modelfields import PhoneNumberField
from django.template.defaultfilters import slugify
import uuid


# Create your models here.
class CustomAccountManager(BaseUserManager):

    def create_user(self, email, password, **other_fields):
        if not email:
            raise ValueError(gettext_lazy('You must enter an email'))
        email = self.normalize_email(email)
        user = self.model(email=email, **other_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **other_fields):
        other_fields.setdefault('is_staff', True)
        other_fields.setdefault('is_superuser', True)
        other_fields.setdefault('is_active', True)
        if other_fields.get('is_staff') is not True:
            raise ValueError('Super User must have "is_staff=True"')
        if other_fields.get('is_superuser') is not True:
            raise ValueError('Super User must have "is_superuser=True"')
        return self.create_user(email, password, **other_fields)


class Customer(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(gettext_lazy('email_address'), unique=True)
    first_name = models.CharField(max_length=150, blank=True, null=True)
    last_name = models.CharField(max_length=150, blank=True, null=True)
    age = models.IntegerField(null=True, blank=True)
    no = models.CharField(max_length=150, blank=True, null=True)
    street = models.CharField(max_length=150, blank=True, null=True)
    country = models.CharField(max_length=150, blank=True, null=True)
    code = models.CharField(max_length=6, blank=True, null=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    objects = CustomAccountManager()
    USERNAME_FIELD = 'email'
    
    def __str__(self):
        try:
            return self.first_name + ' ' + self.last_name
        except:
            return "No Name entered yet."

class Car(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    number_plate = models.CharField(max_length=10, unique=True, blank=True, null=True)
    model = models.CharField(max_length=150, blank=True, null=True)
    brand = models.CharField(max_length=150, blank=True, null=True)

    def __str__(self):
        return self.number_plate

# Create your models here.
class Ad(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    car = models.ForeignKey(Car, on_delete=models.CASCADE)
    date_of_pub = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=255)
    content = models.TextField(max_length=255)
    charges_per_km = models.CharField(max_length=255)
    image = models.ImageField(upload_to="static/images")

    def __str__(self):
        return self.title

    def model(self):
        return self.car.model

    def full_name(self):
        return self.customer.first_name + ' ' + self.customer.last_name

    def brand(self):
        return self.car.brand

class Bike(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    number_plate = models.CharField(max_length=10, unique=True, blank=True, null=True)
    model = models.CharField(max_length=150, blank=True, null=True)
    brand = models.CharField(max_length=150, blank=True, null=True)

    def __str__(self):
        return self.number_plate