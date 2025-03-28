from django.shortcuts import render
from api import serializers as api_serializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework import generics
from userauths.models import User, Profile
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response
from rest_framework import status
import random
from api import models as api_models
from decimal import Decimal
import requests

# this view is for token generation
class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = api_serializer.MyTokenObtainPairSerializer
'''when someone geos to  register endpoint it will come to this endpoint
and it will allow any user to use this endpoint'''

#end point to register a user
class RegisterView(generics.CreateAPIView):
     queryset = User.objects.all()
     permission_classes = [AllowAny] #allows any user to use this endpoint
     serializer_class = api_serializer.RegisterSerializer

#method to generate otp
def generate_random_otp(length=7):
    otp="".join([str(random.randint(0,9)) for _ in range(length)])
    return otp

#how to reset password
class PasswordResetEmailVerifyAPIView(generics.RetrieveAPIView):
    permission_classes=[AllowAny]
    serializer_class=api_serializer.UserSerializer # user model will be modified so we need the serializer to be modified

    def get_object(self):
        email=self.kwargs['email'] #Grabs the email from the URL. for this in the url we need <email>
        user=User.objects.filter(email=email).first()
        if user:
           
            uuidb64=user.pk
            refresh=RefreshToken.for_user(user)
            refresh_token=str(refresh.access_token)
            user.refresh_token=refresh_token
            user.otp=generate_random_otp()
            user.save() # we want to save the otp for the user so using save method
            link=f"http://localhost:3000/create-new-password/?otp={user.otp}&uuidb64={uuidb64}&=refresh_token={refresh_token}"
            print("link=",link)
            return user
        return None
    

class PasswordChangeAPIView(generics.CreateAPIView):
    permission_classes=[AllowAny]
    serializer_class=api_serializer.UserSerializer
   
    def create(self, request, *args, **kwargs):
        payload=request.data
        otp=payload['otp']
        uuidb64=payload['uuidb64']
        password=payload['password']

        user=User.objects.get(id=uuidb64,otp=otp)
        if user:
            user.set_password(password)
            user.otp=""
            user.save()
            return Response({"message":"password changed successfully"},status=200)
        else:
            return Response({"message":"user doesn't exist"},status=400)


class CategoryListAPIView(generics.ListAPIView):
    queryset=api_models.Category.objects.filter(active=True)
    serializer_class=api_serializer.CategorySerializer
    permission_classes=[AllowAny]

class CourseListAPIView(generics.ListAPIView):
    queryset=api_models.Course.objects.filter(platform_status="Published",teacher_course_status="Published")
    serializer_class=api_serializer.CourseSerializer
    permission_classes=[AllowAny]

class CourseDetailAPIView(generics.RetrieveAPIView):
    serializer_class = api_serializer.CourseSerializer
    permission_classes = [AllowAny]
    queryset = api_models.Course.objects.filter(platform_status="Published", teacher_course_status="Published")

    def get_object(self):
        slug = self.kwargs['slug']
        course = api_models.Course.objects.get(slug=slug, platform_status="Published", teacher_course_status="Published")
        return course
    
#adding items to cart
class CartAPIView(generics.CreateAPIView):
    queryset = api_models.Cart.objects.all()
    serializer_class = api_serializer.CartSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        course_id = request.data['course_id']  
        user_id = request.data['user_id']
        price = request.data['price']
        country_name = request.data['country_name']
        cart_id = request.data['cart_id']

        print("course_id ==========", course_id)

        course = api_models.Course.objects.filter(id=course_id).first()
        
        if user_id != "undefined":
            user = User.objects.filter(id=user_id).first()
        else:
            user = None

        try:
            country_object = api_models.Country.objects.filter(name=country_name).first()
            country = country_object.name
        except:
            country_object = None
            country = "United States"

        if country_object:
            tax_rate = country_object.tax_rate / 100
        else:
            tax_rate = 0

        cart = api_models.Cart.objects.filter(cart_id=cart_id, course=course).first()

        if cart:
            cart.course = course
            cart.user = user
            cart.price = price
            cart.tax_fee = Decimal(price) * Decimal(tax_rate)
            cart.country = country
            cart.cart_id = cart_id
            cart.total = Decimal(cart.price) + Decimal(cart.tax_fee)
            cart.save()

            return Response({"message": "Cart Updated Successfully"}, status=status.HTTP_200_OK)

        else:
            cart = api_models.Cart()

            cart.course = course
            cart.user = user
            cart.price = price
            cart.tax_fee = Decimal(price) * Decimal(tax_rate)
            cart.country = country
            cart.cart_id = cart_id
            cart.total = Decimal(cart.price) + Decimal(cart.tax_fee)
            cart.save()

            return Response({"message": "Cart Created Successfully"}, status=status.HTTP_201_CREATED)
        
#cart list api view for getting cart list 
class CartListAPIView(generics.ListAPIView):
    serializer_class = api_serializer.CartSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        cart_id = self.kwargs['cart_id']
        queryset = api_models.Cart.objects.filter(cart_id=cart_id)
        return queryset


#cartItemDelete
class CartItemDeleteAPIView(generics.DestroyAPIView):
    serializer_class = api_serializer.CartSerializer
    permission_classes = [AllowAny]

    def get_object(self):
        cart_id = self.kwargs['cart_id']
        item_id = self.kwargs['item_id']
        return api_models.Cart.objects.filter(cart_id=cart_id, id=item_id).first()
    
#The RetrieveAPIView is used when you want to fetch and return a single instance (or record) of a model rather than a list of items. 


#cart stat api view
class CartStatsAPIView(generics.RetrieveAPIView):
    serializer_class = api_serializer.CartSerializer
    permission_classes = [AllowAny]
    lookup_field = 'cart_id'

    def get_queryset(self):
        cart_id = self.kwargs['cart_id']
        queryset = api_models.Cart.objects.filter(cart_id=cart_id)
        return queryset
    
    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()

        total_price = 0.00
        total_tax = 0.00
        total_total = 0.00

        for cart_item in queryset:
            total_price += float(self.calculate_price(cart_item))
            total_tax += float(self.calculate_tax(cart_item))
            total_total += round(float(self.calculate_total(cart_item)), 2)

        data = {
            "price": total_price,
            "tax": total_tax,
            "total": total_total,
        }

        return Response(data)
    
    #create order api view
    # data to set out this end point
    {
        "full_name": "John Doe", 
        "email":"elaf@gmail.com",
        "country":"United States",
        "cart_id":  "12324",
        "user_id": "1"
    }

    class CreateOrderAPIView(generics.CreateAPIView):
        serializer_class = api_serializer.CartOrderSerializer
        permission_classes = [AllowAny]
        queryset = api_models.CartOrder.objects.all()

        def create(self, request, *args, **kwargs):
            full_name = request.data['full_name']
            email = request.data['email']
            country = request.data['country']
            cart_id = request.data['cart_id']
            user_id = request.data['user_id']

            if user_id != 0:
                user = User.objects.get(id=user_id)
            else:
                user = None

            cart_items = api_models.Cart.objects.filter(cart_id=cart_id)

            total_price = Decimal(0.00)
            total_tax = Decimal(0.00)
            total_initial_total = Decimal(0.00)
            total_total = Decimal(0.00)

            order = api_models.CartOrder.objects.create(
                full_name=full_name,
                email=email,
                country=country,
                student=user
            )

            for c in cart_items:
                api_models.CartOrderItem.objects.create(
                    order=order,
                    course=c.course,
                    price=c.price,
                    tax_fee=c.tax_fee,
                    total=c.total,
                    initial_total=c.total,
                    teacher=c.course.teacher
                )

                total_price += Decimal(c.price)
                total_tax += Decimal(c.tax_fee)
                total_initial_total += Decimal(c.total)
                total_total += Decimal(c.total)

                order.teachers.add(c.course.teacher)

            order.sub_total = total_price
            order.tax_fee = total_tax
            order.initial_total = total_initial_total
            order.total = total_total
            order.save()

            return Response({"message": "Order Created Successfully", "order_oid": order.oid}, status=status.HTTP_201_CREATED)

 
