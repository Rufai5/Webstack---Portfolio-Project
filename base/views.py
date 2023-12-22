from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q 
from django.contrib.auth import authenticate, login, logout
from .models import Course, Topic, Message, User
from .forms import CourseForm, UserForm, MyUserCreationForm
# Create your views here.

# courses = [
#     {'id': 1, 'name': 'Lets learn python together'},
#     {'id': 2, 'name': 'Design together with me'},
#     {'id': 3, 'name': 'Frontend developers'},
# ]

def loginPage(request):
    page = 'login'
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        email = request.POST.get('email').lower()
        password = request.POST.get('password')

        try:
            user = User.objects.get(email=email)
        except:
            messages.error(request, 'User not found in our system.')

        user = authenticate(request, email=email, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
             messages.error(request, 'Username OR password not found in our system.')
         
    context = {'page': page}
    return render(request, 'base/login_register.html', context)

def logoutUser(request):
    logout(request)
    return redirect('home')     

def registerPage(request):
    form = MyUserCreationForm()

    if request.method == 'POST':
        form = MyUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'An error occured during registration')

    return render(request, 'base/login_register.html', {'form': form})

def home(request):
    q= request.GET.get('q') if request.GET.get('q') != None else ''

    courses = Course.objects.filter(
        Q(topic__name__icontains=q) |
        Q(name__icontains=q) |
        Q(description__contains=q)
        )
        

    topics = Topic.objects.all()[0:5]
    course_count = courses.count()
    course_messages = Message.objects.filter(
        Q(course__topic__name__icontains=q))[0:3]

    context =  {'courses': courses, 'topics': topics, 
                'course_count': course_count, 'course_messages': course_messages}
    return render(request, 'base/home.html', context)
    
def course(request, pk):
    course = Course.objects.get(id=pk)
    course_messages = course.message_set.all()
    participants = course.participants.all()

    if request.method == 'POST':
        message = Message.objects.create(
            user=request.user,
            course=course,
            body=request.POST.get('body')
        )
        course.participants.add(request.user)
        return redirect('course', pk=course.id)
    context = {'course': course, 'course_messages': course_messages, 
               'participants':  participants}       
    return render(request, 'base/course.html', context) 

def userProfile(request, pk):
    user = User.objects.get(id=pk)
    courses = user.course_set.all()
    course_messages = user.message_set.all()
    topics = Topic.objects.all()
    context = {'user': user, 'courses': courses, 
               'course_messages': course_messages, 'topics': topics}
    return render(request, 'base/profile.html', context)
 

@login_required(login_url='login')
def createCourse(request):
    form = CourseForm()
    topics = Topic.objects.all()
    if request.method == 'POST':
        topic_name = request.POST.get('topic')
        topic, created = Topic.objects.get_or_create(name=topic_name)

        Course.objects.create(
            host=request.user,
            topic=topic,
            name=request.POST.get('name'),
            description=request.POST.get('description'),
        )
        return redirect('home')

    context = {'form': form, 'topics': topics}
    return render(request, 'base/course_form.html', context)

@login_required(login_url='login')
def updateCourse(request, pk):
    course = Course.objects.get(id=pk)
    form = CourseForm(instance=course)
    topics = Topic.objects.all()
    if request.user != course.host:
        return HttpResponse('Access Denied !!')
    
    if request.method == 'POST':
        topic_name = request.POST.get('topic')
        topic, created = Topic.objects.get_or_create(name=topic_name)
        course.name = request.POST.get('name')
        course.topic = topic
        course.description = request.POST.get('description')
        course.save()
        return redirect('home')

    context = {'form': form, 'topics': topics, 'course': course}
    return render(request, 'base/course_form.html', context)

@login_required(login_url='login')
def deleteCourse(request, pk):
    course = Course.objects.get(id=pk)

    if request.user != course.host:
        return HttpResponse('Access Denied !!')

    if request.method == 'POST':
        course.delete()
        return redirect('home')
    return render(request, 'base/delete.html', {'obj':course})

@login_required(login_url='login')
def deleteMessage(request, pk):
    message = Message.objects.get(id=pk)

    if request.user != message.user:
        return HttpResponse('Access Denied !!')

    if request.method == 'POST':
        message.delete()
        return redirect('home')
    return render(request, 'base/delete.html', {'obj':message})


@login_required(login_url='login')
def updateUser(request):
    user = request.user
    form = UserForm(instance=user)

    if request.method == 'POST':
        form = UserForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            return redirect('user-profile', pk=user.id)

    return render(request, 'base/update-user.html', {'form': form})


def topicsPage(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    topics = Topic.objects.filter(name__icontains=q)
    return render(request, 'base/topics.html', {'topics': topics})


def activityPage(request):
    course_messages = Message.objects.all()
    return render(request, 'base/activity.html', {'course_messages': course_messages})