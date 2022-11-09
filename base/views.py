from .models import *
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from .serializers import *
from rest_framework import status, generics, permissions
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer



@api_view(['GET', 'POST', 'PUT'])
@permission_classes([permissions.IsAuthenticated])
def cars(request, pk=None):
    try:
        if request.method == 'GET':
            if pk:
                car = Car.objects.get(pk=pk)
                if car.customer == request.user:
                    serializer = CarSerializer(car)
                else:
                    return Response("No car found!")
            else:
                cars = Car.objects.filter(customer=request.user)
                serializer = CarSerializer(cars, many=True)
            return Response(serializer.data)
        elif request.method == 'POST':
            car = Car.objects.create(customer=request.user, **request.data.dict())
            serializer = CarSerializer(car)
            return Response(serializer.data)
        elif request.method == 'PUT':
            car = Car.objects.get(pk=pk)
            if car.customer == request.user:
                car.__dict__.update(**request.data.dict())
                car.save()
                serializer = CarSerializer(car)
                return Response(serializer.data)
                # return Response({"success": True})
            else:
                return Response({"success": False})
    except:
        return Response({"success": True})


@api_view(['GET', 'POST', 'PUT', 'DELETE'])
def ads(request, pk=None):
    try:
        if request.method == 'GET':
            if pk:
                ad = Ad.objects.get(pk=pk)
                serializer = AdSerializer(ad)
                return Response(serializer.data)
            else:
                ads = Ad.objects.all()
                serializer = AdSerializer(ads, many=True)
                return Response(serializer.data)
        elif request.method == "POST":
            ad = Ad.objects.create(customer=request.user, title=request.data['title'], 
            content=request.data['content'], charges_per_km=request.data['charges_per_km'],
            image=request.data['image'], car=Car.objects.get(customer=request.user, number_plate=request.data['car']))
            serializer = AdSerializer(ad)
            # return Response(serializer.data)
            return Response({"success": True})
        elif request.method == "DELETE":
            ad = Ad.objects.get(pk=pk)
            if ad.customer == request.user:
                ad.delete()
                return Response({"success": True})
            else:
                return Response({"success": False})
        elif request.method == "PUT":
            ad = Ad.objects.get(pk=pk)
            if ad.customer==request.user:
                ad.__dict__.update(**request.data.dict())
                ad.save()
                serializer = AdSerializer(ad)
                return Response({"success": True})
                # return Response(serializer.data)
            else:
                return Response({"success": False})
    except:
        return Response({"success": False})


# Create your views here.
class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, customer):
        token = super().get_token(customer)

        # Add custom claims
        token['email'] = customer.email
        token['password'] = customer.password
        # ...

        return token


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer

class RegisterAPI(generics.GenericAPIView):
    serializer_class = RegisterSerializer

    def post(self, request, *args, **kwargs):
        c = Customer.objects.filter(email=request.data['email'])
        if len(c) > 0:
            return Response({"message": 'Email already registered! Try a new email!'}, status.HTTP_200_OK)
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            customer = serializer.save()
            return Response({
                "status": status.HTTP_200_OK,
                "message": 'An Email has been sent to your email ID if it was valid.',
                "user": CustomerSerializer(customer, context=self.get_serializer_context()).data,
            })
        return Response({"Errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['PUT'])
@permission_classes([permissions.IsAuthenticated])
def update_customer(request):
    try:
        customer = Customer.objects.get(pk=request.user.pk)
        e = customer.email
        print(customer.password)
        x = request.data.dict()
        if "email" in x:
            del x['email']
        if "password" in x:
            del x['password']
        customer.__dict__.update(**x)
        customer.save()    
        serializer = CustomerSerializer(customer)
        # return Response(serializer.data)
        return Response({"success": True})
    except:
        return Response({"success": False})