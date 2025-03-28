# Import Django's password validation
from django.contrib.auth.password_validation import validate_password
# Import your API models
from api import models as api_models

# Import DRF serializers and the JWT serializer
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

# Import user-related models
from userauths.models import Profile, User

# ------------------------------------------------------------------------------
# Custom JWT Token Serializer
# This serializer customizes the JWT payload by including additional user fields.
class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        # Get the default token from the superclass
        token = super().get_token(user)

        # Add custom claims to the token
        token['full_name'] = user.full_name
        token['email'] = user.email
        token['username'] = user.username
        
        # Attempt to include teacher id if user is a teacher; otherwise, default to 0
        try:
            token['teacher_id'] = user.teacher.id
        except:
            token['teacher_id'] = 0

        return token

# ------------------------------------------------------------------------------
# User Registration Serializer
# Validates registration data and creates a new user.
class RegisterSerializer(serializers.ModelSerializer):
    # Define password fields with validation
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        # Only include these fields for registration
        fields = ['full_name', 'email', 'password', 'password2']

    def validate(self, attr):
        # Ensure the two passwords match
        if attr['password'] != attr['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})
        return attr
    
    def create(self, validated_data):
        # Create the user instance with provided full_name and email
        user = User.objects.create(
            full_name=validated_data['full_name'],
            email=validated_data['email'],
        )

        # Derive username from email (part before the '@')
        email_username, _ = user.email.split("@")
        user.username = email_username
        # Set and hash the password
        user.set_password(validated_data['password'])
        user.save()
        return user

# ------------------------------------------------------------------------------
# User Serializer: Serializes all fields of the User model.
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

# ------------------------------------------------------------------------------
# Profile Serializer: Serializes all fields of the Profile model.
class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = "__all__"

# ------------------------------------------------------------------------------
# Category Serializer: Serializes specific fields of the Category model.
class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        fields = ['id', 'title', 'image', 'slug', 'course_count']
        model = api_models.Category

# ------------------------------------------------------------------------------
# Teacher Serializer: Serializes Teacher model including related methods fields.
class TeacherSerializer(serializers.ModelSerializer):
    class Meta:
        fields = [
            "user", "image", "full_name", "bio", "facebook", 
            "twitter", "linkedin", "about", "country", "students", "courses", "review",
        ]
        model = api_models.Teacher

# ------------------------------------------------------------------------------
# VariantItem Serializer: Serializes all fields of VariantItem model.
# Adjusts the serialization depth based on the request method.
class VariantItemSerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = api_models.VariantItem

    def __init__(self, *args, **kwargs):
        super(VariantItemSerializer, self).__init__(*args, **kwargs)
        # Adjust depth dynamically depending on request method.
        request = self.context.get("request")
        if request and request.method == "POST":
            self.Meta.depth = 0
        else:
            self.Meta.depth = 3

# ------------------------------------------------------------------------------
# Variant Serializer: Serializes Variant model including nested variant items.
class VariantSerializer(serializers.ModelSerializer):
    # Nested serializers for variant_items and items (both many=True indicates a list)
    variant_items = VariantItemSerializer(many=True)
    items = VariantItemSerializer(many=True)
    
    class Meta:
        fields = '__all__'
        model = api_models.Variant

    def __init__(self, *args, **kwargs):
        super(VariantSerializer, self).__init__(*args, **kwargs)
        request = self.context.get("request")
        if request and request.method == "POST":
            self.Meta.depth = 0
        else:
            self.Meta.depth = 3

# ------------------------------------------------------------------------------
# Question_Answer_Message Serializer: Serializes messages in a Q&A thread.
# Includes the nested profile for additional user details.
class Question_Answer_MessageSerializer(serializers.ModelSerializer):
    # Include profile details using the ProfileSerializer. many=False because each message has one profile.
    profile = ProfileSerializer(many=False)

    class Meta:
        fields = '__all__'
        model = api_models.Question_Answer_Message

# ------------------------------------------------------------------------------
# Question_Answer Serializer: Serializes the main question along with its messages.
# Nesting the messages using Question_Answer_MessageSerializer with many=True as there can be multiple replies.
class Question_AnswerSerializer(serializers.ModelSerializer):
    # 'messages' is a list of message objects associated with the question.
    messages = Question_Answer_MessageSerializer(many=True)
    # Include the profile of the user who asked the question.
    profile = ProfileSerializer(many=False)
    
    class Meta:
        fields = '__all__'
        model = api_models.Question_Answer

# ------------------------------------------------------------------------------
# Cart Serializer: Serializes all fields of the Cart model.
# Adjusts serialization depth based on the request method.
class CartSerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = api_models.Cart

    def __init__(self, *args, **kwargs):
        super(CartSerializer, self).__init__(*args, **kwargs)
        request = self.context.get("request")
        if request and request.method == "POST":
            self.Meta.depth = 0
        else:
            self.Meta.depth = 3

# ------------------------------------------------------------------------------
# CartOrderItem Serializer: Serializes all fields of the CartOrderItem model.
# Adjusts depth dynamically.
class CartOrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = api_models.CartOrderItem

    def __init__(self, *args, **kwargs):
        super(CartOrderItemSerializer, self).__init__(*args, **kwargs)
        request = self.context.get("request")
        if request and request.method == "POST":
            self.Meta.depth = 0
        else:
            self.Meta.depth = 3

# ------------------------------------------------------------------------------
# CartOrder Serializer: Serializes the CartOrder model and nests its order items.
class CartOrderSerializer(serializers.ModelSerializer):
    # 'order_items' is a list of CartOrderItem objects in the order.
    order_items = CartOrderItemSerializer(many=True)
    
    class Meta:
        fields = '__all__'
        model = api_models.CartOrder

    def __init__(self, *args, **kwargs):
        super(CartOrderSerializer, self).__init__(*args, **kwargs)
        request = self.context.get("request")
        if request and request.method == "POST":
            self.Meta.depth = 0
        else:
            self.Meta.depth = 3

# ------------------------------------------------------------------------------
# Certificate Serializer: Serializes all fields of the Certificate model.
class CertificateSerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = api_models.Certificate

# ------------------------------------------------------------------------------
# CompletedLesson Serializer: Serializes all fields of the CompletedLesson model.
# Adjusts depth dynamically.
class CompletedLessonSerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = api_models.CompletedLesson

    def __init__(self, *args, **kwargs):
        super(CompletedLessonSerializer, self).__init__(*args, **kwargs)
        request = self.context.get("request")
        if request and request.method == "POST":
            self.Meta.depth = 0
        else:
            self.Meta.depth = 3

# ------------------------------------------------------------------------------
# Note Serializer: Serializes all fields of the Note model.
class NoteSerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = api_models.Note

# ------------------------------------------------------------------------------
# Review Serializer: Serializes all fields of the Review model.
# Includes the nested profile for reviewer details.
class ReviewSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer(many=False)

    class Meta:
        fields = '__all__'
        model = api_models.Review

    def __init__(self, *args, **kwargs):
        super(ReviewSerializer, self).__init__(*args, **kwargs)
        request = self.context.get("request")
        if request and request.method == "POST":
            self.Meta.depth = 0
        else:
            self.Meta.depth = 3

# ------------------------------------------------------------------------------
# Notification Serializer: Serializes all fields of the Notification model.
class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = api_models.Notification

# ------------------------------------------------------------------------------
# Coupon Serializer: Serializes all fields of the Coupon model.
class CouponSerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = api_models.Coupon

# ------------------------------------------------------------------------------
# Wishlist Serializer: Serializes all fields of the Wishlist model.
# Adjusts depth dynamically.
class WishlistSerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = api_models.Wishlist

    def __init__(self, *args, **kwargs):
        super(WishlistSerializer, self).__init__(*args, **kwargs)
        request = self.context.get("request")
        if request and request.method == "POST":
            self.Meta.depth = 0
        else:
            self.Meta.depth = 3

# ------------------------------------------------------------------------------
# Country Serializer: Serializes all fields of the Country model.
class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = api_models.Country

# ------------------------------------------------------------------------------
# EnrolledCourse Serializer: Serializes the EnrolledCourse model with nested related fields.
class EnrolledCourseSerializer(serializers.ModelSerializer):
    lectures = VariantItemSerializer(many=True, read_only=True)
    completed_lesson = CompletedLessonSerializer(many=True, read_only=True)
    curriculum = VariantSerializer(many=True, read_only=True)
    note = NoteSerializer(many=True, read_only=True)
    question_answer = Question_AnswerSerializer(many=True, read_only=True)
    # 'review' is a single object, so many=False
    review = ReviewSerializer(many=False, read_only=True)

    class Meta:
        fields = '__all__'
        model = api_models.EnrolledCourse

    def __init__(self, *args, **kwargs):
        super(EnrolledCourseSerializer, self).__init__(*args, **kwargs)
        request = self.context.get("request")
        if request and request.method == "POST":
            self.Meta.depth = 0
        else:
            self.Meta.depth = 3

# ------------------------------------------------------------------------------
# Course Serializer: Serializes the Course model with nested relationships.
class CourseSerializer(serializers.ModelSerializer):
    # 'students' is a list of EnrolledCourse objects associated with the course.
    students = EnrolledCourseSerializer(many=True, required=False, read_only=True)
    # 'curriculum' and 'lectures' are lists of objects related to the course.
    curriculum = VariantSerializer(many=True, required=False, read_only=True)
    lectures = VariantItemSerializer(many=True, required=False, read_only=True)
    reviews = ReviewSerializer(many=True, read_only=True, required=False)
    
    class Meta:
        fields = [
            "id", "category", "teacher", "file", "image", "title", "description", 
            "price", "language", "level", "platform_status", "teacher_course_status", 
            "featured", "course_id", "slug", "date", "students", "curriculum", "lectures", 
            "average_rating", "rating_count", "reviews",
        ]
        model = api_models.Course

    def __init__(self, *args, **kwargs):
        super(CourseSerializer, self).__init__(*args, **kwargs)
        request = self.context.get("request")
        if request and request.method == "POST":
            self.Meta.depth = 0
        else:
            self.Meta.depth = 3

# ------------------------------------------------------------------------------
# Student Summary Serializer: A simple serializer (not model-based) for summarizing student data.
class StudentSummarySerializer(serializers.Serializer):
    total_courses = serializers.IntegerField(default=0)
    completed_lessons = serializers.IntegerField(default=0)
    achieved_certificates = serializers.IntegerField(default=0)

# ------------------------------------------------------------------------------
# Teacher Summary Serializer: A simple serializer for summarizing teacher data.
class TeacherSummarySerializer(serializers.Serializer):
    total_courses = serializers.IntegerField(default=0)
    total_students = serializers.IntegerField(default=0)
    total_revenue = serializers.IntegerField(default=0)
    monthly_revenue = serializers.IntegerField(default=0)
