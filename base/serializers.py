from .models import *
from rest_framework import serializers

class CustomerSerializer(serializers.ModelSerializer):

    class Meta:
        model = Customer
        exclude = ('is_staff', "last_login", "password", "is_superuser", "groups", "user_permissions")

class RegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=100, min_length=6)
    password = serializers.CharField(max_length=100)
    
    class Meta:
        model = Customer
        fields = ('id', 'email', 'password', "first_name", "last_name", "created_at"
                    , "age", "no", "street", "country", "code")
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        customer = Customer.objects.create(**validated_data)
        customer.set_password(validated_data['password'])
        customer.save()
        return customer


class CarSerializer(serializers.ModelSerializer):
    customer = CustomerSerializer()

    class Meta:
        model = Car
        fields = '__all__'

class AdSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Ad
        fields = ['full_name', "date_of_pub", "title", "content", "charges_per_km", "image", "model", "brand"]



