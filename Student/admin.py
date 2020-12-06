from django.contrib import admin

# Register your models here.
from django.contrib import admin
from Student.models import Student, User, Course, FileType, Post

# Register your models here.
admin.site.register(Student)
admin.site.register(Course)
admin.site.register(FileType)
admin.site.register(Post)

