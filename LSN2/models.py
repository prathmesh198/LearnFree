from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    fullname = models.CharField(max_length=255)
    course = models.ForeignKey('course', on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.user.username
class user(models.Model):
    primary_key = models.AutoField(unique=True, primary_key=True)
    fullname = models.CharField(max_length=255,default="")
    username = models.CharField(max_length=100,unique=True)
    password = models.CharField(max_length=100,unique=True)
    email= models.EmailField(max_length=100,unique=True)
    course=models.ForeignKey('course', on_delete=models.SET_NULL, null=True, blank=True)   
def __str__(self):
    return self.username    



class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    fullname = models.CharField(max_length=255)
    course = models.ForeignKey('course', on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.user.username



class course(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    photo= models.ImageField(upload_to='course_photos/')
    pdf= models.FileField(upload_to='course_pdfs/')
def __str__(self):
    return f"{self.photo} - {self.description}"






class Module(models.Model):
    course = models.ForeignKey(
        course,
        on_delete=models.CASCADE,
        related_name='modules'  
    )
    title = models.CharField(max_length=200)
    content = models.TextField()

    def __str__(self):
        return self.title
