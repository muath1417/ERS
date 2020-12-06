import os

from PIL import Image
from django.core.validators import FileExtensionValidator
from django.db import models

# Create your models here.

from django.db import models
from django.utils import timezone
from user_unique_email.models import User

from Student.storage import OverwriteStorage


class Student(User):
    accept = models.BooleanField()
    fixture = ['Student.json']

    def __str__(self):
        return 'Student {} : {} : {}'.format(self.username,self.email,self.accept)


class Course(models.Model):
    def upload_to(self,filename):
        return "courses/{}.{}".format(self.name,filename.split('.')[-1])

    fixture = ['Course.json']
    name = models.CharField(max_length=200)
    description = models.CharField(max_length=400)
    image = models.ImageField(upload_to=upload_to,default='courses/course.png',storage=OverwriteStorage())
    created_at = models.DateTimeField(auto_now_add=True,null=True)
    updated_at = models.DateTimeField(auto_now=True,null=True)

    def __str__(self):
        return '{} : {}'.format(self.name, self.description)

    def save(self):
        super(Course, self).save()
        img = Image.open(self.image.path)  # Open image using self
        new_size = (530, 530)
        new_img = img.resize(new_size,Image.ANTIALIAS)
        new_img.save(self.image.path)
        print(new_img)


class FileType(models.Model):
    FILE_CHOICES = (
        ("docs", "Documents"),
        ("image", "Images"),
        ("file", "File"),
        ("link", "URL LINK"),
        ("zip", "Archive"),
    )

    fixtures = ['Course.json']
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=100)
    category = models.CharField(choices=FILE_CHOICES,max_length=20,default="image")

    def __str__(self):
        return '{} : {}'.format(self.name, self.category)


class Post(models.Model):
    def upload_to(self,filename):
        return "posts/{}_{}_{}.{}".format(self.course.id,self.student.id,str(timezone.now()),filename.split('.')[-1])

    title = models.CharField(max_length=150)
    content = models.CharField(max_length=500)
    file = models.FileField(upload_to=upload_to,validators=[FileExtensionValidator(allowed_extensions=['pdf', 'doc', 'docx', 'jpg', 'png', 'xlsx', 'xls','zip','7z','rar','mp4','avi','mp3'],message="These extension not allowed sorry")])
    file_type = models.ForeignKey(FileType, on_delete=models.CASCADE)
    publish_date = models.DateTimeField('publish_date', default=timezone.now())
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    course = models.ForeignKey(Course,on_delete=models.CASCADE)
    likes = models.ManyToManyField('Student.Student', related_name='post_likes', blank=True)
    dislikes = models.ManyToManyField('Student.Student', related_name='post_dislikes', blank=True)

    def __str__(self):
        return 'Post: {} : {} {} '.format(self.title, self.student,self.content)

