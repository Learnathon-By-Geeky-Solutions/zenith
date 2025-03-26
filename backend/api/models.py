from django.db import models
from userauths.models import User,Profile
from django.utils.text import slugify
from shortuuidfield   import ShortUUIDField
from django.utils import timezone

LANGUAGE= (   
('English','English'),
('French','French'),
('Spanish','Spanish'),
('German','German'), 
('Chinese','Chinese'),
('Japanese','Japanese'),
('Russian','Russian'),
('Arabic','Arabic'),
('Hindi','Hindi'),
('Bengali','Bengali'),
('Portuguese','Portuguese'),
)
LEVEL= (    
('Beginner','Beginner'),
('Intermediate','Intermediate'),
('Advanced','Advanced'),
('Expert','Expert'),
('All','All'),
)
TEACHER_STATUS= (
('Draft','Draft'),
('Published','Published'),
('Unpublished','Unpublished'),
)

PLATFORM_STATUS=(
('Draft','Draft'),
('Published','Published'),
('Unpublished','Unpublished'),
)

#teacher model
class Teacher(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    image = models.FileField(upload_to='course -file',null=True,blank=True,default='default.jpg')
    full_name = models.CharField(max_length=100)  
    bio = models.CharField(max_length=100)  
    facebook = models.URLField(max_length=100,blank=True)
    twitter = models.URLField(max_length=100,blank=True)
    about = models.TextField(null=True,blank=True)
    country = models.CharField(max_length=100)
    

    def __str__(self):
        return self.full_name

    #this will return the number of students a teacher has
    def student_count(self):
        return CartOderItem.objects.filter(teacher=self)

    #this will return all the courses of the teacher
    def courses(self):
        return Course.objects.filter(teacher=self)
    
    #this will return the review 
    def review(self):
        return Course.objects.filter(teacher=self).count()
    
    
class Category(models.Model):
    title = models.CharField(max_length=100)
    image = models.FileField(upload_to='course -file',null=True,blank=True,default='default.jpg')
    slug = models.SlugField(unique=True,null=True,blank=True)
    
    class Meta:
        verbose_name_plural = 'Category'
        ordering = ['title']
    
    def __str__(self):
        return self.title
    
    def course_count(self):
        return Course.objects.filter(category=self).count()
    
    def save(self, *args, **kwargs):
        if self.slug == "" or self.slug is None:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

class Course(models.Model):
    category= models.ForeignKey(Category,on_delete=models.SET_NULL,null=True,blank=True),
    teacher=models.ForeignKey(Teacher,on_delete=models.CASCADE)
    file=models.FileField(upload_to='course -file',null=True,blank=True)
    image=models.FileField(upload_to='course -file',null=True,blank=True)
    title=models.CharField(max_length=100)
    description=models.TextField(null=True,blank=True)
    price=models.DecimalField(max_digit=10,decimal_places=2)
    language=models.CharField(choices=LANGUAGE,max_length=100,default='English')
    language=models.CharField(choices=LEVEL,max_length=100,default='Beginner')
    platform_status=models.CharField(choices=PLATFORM_STATUS,max_length=100,default='Published')
    teacher_course_status=models.CharField(choices=TEACHER_STATUS,max_length=100,default='Published')
    featured=models.BooleanField(default=False)
    course_id=ShortUUIDField(unique=True,length=6,max_length=20,alphabet='0123456789')
    slug=models.SlugField(unique=True,null=True,blank=True)
    date=models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if self.slug == "" or self.slug is None:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    #all the students enrolled in the course
    def students(self):
        return EnrolledCourse.objects.filter(course=self)
    
    def curriculum(self):
        return  VariantItem.objects.filter(variant_course=self)
    
    def lectures(self):
        return  VariantItem.objects.filter(variant_course=self)
    
    def average_rating(self):
        average_rating=Review.objects.filter(course=self,active=True).aggregate(average_rating=models.Avg('rating'))
        return average_rating['average_rating']
    
    def rating_count(self):
        return Review.objects.filter(course=self,active=True).count()
    
    def reviews(self):
        return Review.objects.filter(course=self,active=True)
    

class Variant(models.Model):
    
    
    

    