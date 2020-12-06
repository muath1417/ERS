from PIL import Image
from PIL.Image import Image
from django.db.models.functions import Concat
from django.shortcuts import render, redirect

# Create your views here.
from django.shortcuts import render
from Student.forms import StudentRegisterForm, StudentLoginForm, StudentPostForm, StudentPasswordChangeForm
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout, update_session_auth_hash
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.utils import timezone
from Student.models import Student, Course, FileType, Post
from django.db.models import Value, ExpressionWrapper, CharField, F, Q


def index(request):
    if request.student.is_authenticated:
        student = request.student
        courses = Course.objects.all()
        file_types = FileType.objects.all()
        context = {}
        context['student'] = student
        context['courses'] = courses
        context['file_types'] = file_types
        print("Student:", student)
        return render(request, 'Student/my_timeline.html', context)
    else:
        return render(request, 'Student/index.html')


@login_required
def courses(request):
    if request.student.is_authenticated:
        student = request.student
        courses = Course.objects.all()
        file_types = FileType.objects.all()
        context = {}
        context['student'] = student
        context['courses'] = courses
        context['file_types'] = file_types
        print("Student:", student)
        return render(request, 'Student/courses.html', context)
    else:
        return render(request, 'Student/index.html')


def about(request):
    context = {}
    if request.student.is_authenticated:
        student = request.student
        courses = Course.objects.all()
        file_types = FileType.objects.all()
        context['student'] = student
        context['courses'] = courses
        context['file_types'] = file_types
        print("Student:", student)

    return render(request, 'Student/about.html', context)


def guidelines(request):
    context = {}
    if request.student.is_authenticated:
        student = request.student
        courses = Course.objects.all()
        file_types = FileType.objects.all()
        context['student'] = student
        context['courses'] = courses
        context['file_types'] = file_types
        print("Student:", student)

    return render(request, 'Student/guidelines.html', context)


def login(request):
    if request.method == 'POST':
        login_form = StudentLoginForm(data=request.POST)
        email = request.POST.get('email')
        password = request.POST.get('password')
        if Student.objects.filter(email=email).first() is not None:
            username = Student.objects.filter(email=email).first().username
            student = authenticate(username=username, password=password)
            if student:
                if student.is_active:
                    auth_login(request, student)
                    return HttpResponseRedirect(reverse('index'))
                else:
                    return render(request, 'Student/login.html',
                                  {'login_form': login_form, 'message': 'account inactive'})
            else:
                print("Someone tried to login and failed.")
                print("They used email: {} and password: {}".format(email, password))

        else:
            print("Someone tried to login and failed.")
            print("They used email: {} and password: {}".format(email, password))


            return render(request, 'Student/login.html', {'login_form': login_form, 'message': 'Invalid Login Details'})

    else:
        login_form = StudentLoginForm()
    return render(request, 'Student/login.html', {'login_form': login_form})


@login_required
def logout(request):
    auth_logout(request)
    return HttpResponseRedirect(reverse('index'))


@login_required
def password_change(request):
    password_changed = False
    if request.method == 'POST':
        form = StudentPasswordChangeForm(student=request.student, data=request.POST)
        if form.is_valid():
            print("form valid")
            print(request.POST)
            password = request.POST["new_password1"]
            request.student.set_password(password)
            request.student.save()
            update_session_auth_hash(request, form.student)
            password_changed = True
        else:
            print("form invalid")
            print(form.errors)
    else:
        form = StudentPasswordChangeForm(student=request.student)

    student = request.student
    courses = Course.objects.all()
    return render(request, 'Student/password_change_form.html',
                  {'form': form, 'student': student, 'courses': courses, 'password_changed': password_changed})


def register(request):
    registered = False
    if request.method == 'POST':
        post = request.POST.copy()
        post['username'] = post['email'].split("@")[0]
        request.POST = post
        print(request.POST.dict(), request.FILES.dict())
        student_register_form = StudentRegisterForm(request.POST, request.FILES)
        if student_register_form.is_valid() :
            student = student_register_form.save()
            student.set_password(student.password)
            student.save()
            registered = True
            auth_login(request, student)
            return HttpResponseRedirect(reverse('index'))
        else:
            print(student_register_form.errors)
    else:
        student_register_form = StudentRegisterForm()



    return render(request, 'Student/registration.html',
                  {'student_register_form': student_register_form,
                   'registered': registered})


@login_required
def profile(request):
    print("profile")
    registered = False
    if request.method == 'POST':
        print(request.POST.dict(), request.FILES.dict())
        student_register_form = StudentRegisterForm(request.POST, request.FILES)
        student_register_form.data['username'] = student_register_form.data['email'].split("@")[0]
        if student_register_form.is_valid():
            student = student_register_form.save()
            student.save()
            registered = True
            return HttpResponseRedirect(reverse('index'))
        else:
            print(student_register_form.errors)
    else:
        student_register_form = StudentRegisterForm(instance=request.student)

    student = request.student
    context = {}
    context['student'] = student
    context['courses'] = Course.objects.all()
    context['student_register_form'] = student_register_form
    return render(request, 'Student/profile.html', context)


@login_required
def my_timeline(request):
    if request.student.is_authenticated:
        student = request.student

        posts = Post.objects.filter(student=student)
        file_types = FileType.objects.all()
        context = {}
        context['student'] = student
        context['courses'] = Course.objects.all()
        context['file_types'] = file_types
        context['posts'] = posts
        print("Timeline:", posts)
        return render(request, 'Student/my_timeline.html', context)
    else:
        return redirect("index")


def post_to_my_timeline(request):
    if request.student.is_authenticated and request.method == 'POST':
        student = request.student
        print(request.POST.dict())
        file_types = FileType.objects.all()
        course = Course.objects.filter(id=request.POST['course']).first()
        student_post_form = StudentPostForm(request.POST, request.FILES)
        if course is not None and student is not None:
            if student_post_form.is_valid():
                print("student post form is valid")
                student_post_form.save()
                course.updated_at = timezone.now()
                course.save()
                print(course)
                posts = Post.objects.filter(student=student)
                context = {}
                context['student'] = student
                context['courses'] = Course.objects.all()
                context['file_types'] = file_types
                context['posts'] = posts
                print("Timeline:", posts)
                return render(request, 'Student/my_timeline.html', context)

            else:
                print("2.else:", student_post_form.errors)
                posts = Post.objects.filter(student=student)
                context = {}
                context['errors'] = student_post_form.errors
                context['student'] = student
                context['courses'] = Course.objects.all()
                context['file_types'] = file_types
                context['posts'] = posts
                print("Timeline:", posts)
                return render(request, 'Student/my_timeline.html', context)

        else:
            print("3.Else:", student_post_form.errors)
            posts = Post.objects.filter(student=student)
            context = {}
            context['errors'] = student_post_form.errors
            context['student'] = student
            context['courses'] = Course.objects.all()
            context['file_types'] = file_types
            context['posts'] = posts
            print("Timeline:", posts)
            return render(request, 'Student/my_timeline.html', context)
    elif request.student.is_authenticated and request.method == 'GET':
        posts = Post.objects.filter(student=request.student)
        file_types = FileType.objects.all()
        context = {}
        context['student'] = request.student
        context['courses'] = Course.objects.all()
        context['file_types'] = file_types
        context['posts'] = posts
        print("Timeline:", posts)
        return render(request, 'Student/my_timeline.html', context)
    else:
        return redirect("index")


@login_required
def timeline(request, course_id):
    if request.student.is_authenticated:
        student = request.student
        course = Course.objects.filter(id=course_id).first()

        if course is not None:
            posts = Post.objects.filter(course=course)
            file_types = FileType.objects.all()
            context = {}
            context['student'] = student
            context['chomeourse'] = course
            context['courses'] = Course.objects.all()
            context['course'] = course
            context['file_types'] = file_types
            context['posts'] = posts
            print("Timeline:", posts)
            return render(request, 'Student/timeline.html', context)

        else:
            return redirect("index")

    else:
        return redirect("index")


def post_to_timeline(request, course_id, student_id):
    if request.student.is_authenticated:
        student = request.student
        course = Course.objects.filter(id=course_id).first()
        student_post_form = StudentPostForm(request.POST, request.FILES)

        if course is not None and student is not None:
            if student_post_form.is_valid():
                print("student post form is valid")
                student_post_form.save()
                course.updated_at = timezone.now()
                course.save()
                print(course)
            else:
                print(student_post_form.errors)

            posts = Post.objects.filter(course=course)
            file_types = FileType.objects.all()
            context = {}
            context['student'] = student
            context['course'] = course
            context['courses'] = Course.objects.all()
            context['file_types'] = file_types
            context['posts'] = posts
            print("Timeline:", posts)
            return render(request, 'Student/timeline.html', context)

        else:
            return redirect("index")

    else:
        return redirect("index")


@login_required
def like_post(request, post_id):
    student = request.student
    post = Post.objects.filter(id=post_id).first()
    print(post.likes.all().count())
    student = Student.objects.get(id=student.id)
    if post.likes.filter(email=student.email).count() >= 1:
        post.likes.remove(student)
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    else:
        post.likes.add(student)
        post.save()
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@login_required
def dislike_post(request, post_id):
    student = request.student
    post = Post.objects.filter(id=post_id).first()
    print(post.dislikes.all().count())
    if post.dislikes.filter(email=student.email).count() >= 1:
        post.dislikes.remove(student)
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    else:
        post.dislikes.add(student)
        post.save()
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@login_required
def delete_post(request, post_id):
    print(request.META.get('HTTP_REFERER'))
    student = request.student
    post = Post.objects.filter(id=post_id).filter(student=student).first()
    print(post)
    if post is not None:
        student = Student.objects.get(id=student.id)
        post.file.delete()
        post.delete()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def search(request):
    name = request.GET['name']
    student = request.student
    base_url = '/timeline/'
    base_image = '/media/'

    courses = Course.objects.filter(name__icontains=name).all().annotate(
        course_url=Concat(Value(base_url), 'id', output_field=CharField())).annotate(
        image_url=Concat(Value(base_image), 'image', output_field=CharField()))

    data = {
        "results": list(courses.values('name', 'description', 'image_url', 'course_url')),
        "name": "Course result",
    }
    print(data)
    return JsonResponse(data)


def search_posts(request):
    name = request.GET['name']
    student = request.student
    base_url = '/get_posts/'+name
    base_image = '/media/'

    posts = Post.objects.filter(Q(content__icontains=name) | Q(title__icontains=name)).all().annotate(
        post_url=Value(base_url,output_field=CharField()))
    data = {
        "results": list(posts.values('title','content', 'course', 'post_url', 'student')),
        "name": "Post result",
    }
    print(data)
    return JsonResponse(data)



def get_posts(request,name):
    student = request.student
    if student.is_authenticated:
        student = request.student
        course = Course.objects.filter().first()

        if course is not None:
            posts = Post.objects.filter(Q(content__icontains=name) | Q(title__icontains=name)).all()
            file_types = FileType.objects.all()
            context = {}
            context['student'] = student
            context['course'] = course
            context['courses'] = Course.objects.all()
            context['course'] = course
            context['file_types'] = file_types
            context['posts'] = posts
            print("Timeline:", posts)
            return render(request, 'Student/timeline.html', context)

        else:
            return redirect("index")

    else:
        return redirect("index")

