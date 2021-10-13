from django.shortcuts import render, HttpResponseRedirect
from .forms import SignUpForm, LoginForm, PostForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from .models import Post, Contact
from django.contrib.auth.models import Group


# home
def home(request):
    posts = Post.objects.all()
    return render(request, 'blog/home.html', {'posts':posts})
    

# All Post Contents
def allposts(request, slug=None):
    posts = Post.objects.all()
    return render(request, 'blog/allposts.html', {'posts':posts})

# About
def about(request):
    return render(request, 'blog/about.html')

# Contact
def contact(request):
    if request.method == 'POST':
        
        name = request.POST['name']
        email = request.POST['email']
        phone = request.POST['phone']
        message = request.POST['message']

        if len(name)<3 or len(email)<3 or len(phone)<10 or len(message)<5:
            messages.error(request, "Please fill correct data")
        else:
            contact = Contact(name=name, email=email, phone=phone, message=message)
            contact.save()
            messages.success(request, "Your message has been sucessfully sent")
    return render(request, 'blog/contact.html')
    

# Dashboard
def dashboard(request):
    if request.user.is_authenticated:
        posts = Post.objects.all()
        user = request.user
        full_name = user.get_full_name()
        gps = user.groups.all()
        return render(request, 'blog/dashboard.html', {'posts':posts, 'full_name':full_name, 'groups':gps})
    else:
        return HttpResponseRedirect('/login/')

    return render(request, 'blog/dashboard.html')

# Logout
def user_logout(request):
    logout(request)
    return HttpResponseRedirect('/')

# Signup
def user_signup(request):
    if request.method =="POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            messages.success(request, 'Congratulations!!! Now you are a Writer Login to continue.')
            user = form.save()
            group = Group.objects.get(name='Writer')
            return HttpResponseRedirect('/login/')
    else:
        form = SignUpForm()
    return render(request, 'blog/signup.html',{'form':form})

# Login
def user_login(request):
    if not request.user.is_authenticated:
        if request.method == "POST":
            form = LoginForm(request=request, data=request.POST)
            if form.is_valid():
                uname = form.cleaned_data['username']
                upass = form.cleaned_data['password']
                user = authenticate(username=uname, password=upass)
                if user is not None:
                    login(request, user)
                    messages.success(request, 'Logged in sucessfully!!!')
                    return HttpResponseRedirect('/dashboard/')
        else:
            form = LoginForm()
        return render(request, 'blog/login.html', {'form':form})
    else:
        return HttpResponseRedirect('/dashboard/')

# Add New Post
def add_post(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            form = PostForm(request.POST, request.FILES)
            if form.is_valid():
                title = form.cleaned_data['title']
                desc = form.cleaned_data['desc']
                author = form.cleaned_data['author']
                title_tag = form.cleaned_data['title_tag']
                post_image = form.cleaned_data['post_image']
                pst = Post(title=title, desc=desc, title_tag=title_tag,  post_image=post_image)
                pst.save()
                form = PostForm()
        else:
            form = PostForm()
        return render(request, 'blog/addpost.html', {'form':form})
    else:
        return HttpResponseRedirect('/login/')

# Update/Edit Post
def update_post(request, id):
    if request.user.is_authenticated:
        if request.method == 'POST':
            pi = Post.objects.get(pk=id)
            form = PostForm(request.POST, instance=pi)
            if form.is_valid():
                form.save()
        else:
            pi = Post.objects.get(pk=id)
            form = PostForm(instance=pi)
        return render(request, 'blog/updatepost.html', {'form':form})
    else:
        return HttpResponseRedirect('/login/')

# Delete Post
def delete_post(request, id):
    if request.user.is_authenticated:
        if request.method == 'POST':
            pi = Post.objects.get(pk=id)
            pi.delete()
            return HttpResponseRedirect('/dashboard/')
    else:
        return HttpResponseRedirect('/login/')

# Mobiles
def mobile(request, slug):
    post = Post.objects.filter(slug=slug).first()
    post.save()
    context = {'post': post, 'user': request.user}
    return render(request, 'blog/mobile.html', context)
    