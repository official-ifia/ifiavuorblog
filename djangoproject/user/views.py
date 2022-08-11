import email
from django.shortcuts import render, redirect
from django.contrib import messages
# from django.contrib.auth.forms import UserCreationForm
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm
from django.contrib.auth.decorators import login_required
from blog.models import Posts
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.core.mail import send_mail
from django.conf import settings

# Create your views here.

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            last = form.cleaned_data.get('last_name')
            form.save()
            subject = f'Welcome {last}'
            message = 'Thanks for joining aproko doctor blog'
            email = form.cleaned_data.get('email')
            send_mail(subject,message,settings.EMAIL_HOST_USER, [email])
            messages.success(request,f'{last} registration successful')
            return redirect('login')
    else:
        form = UserRegisterForm()
    context = {'form':form}
    return render(request, 'user/register.html', context)

@login_required
def profile(request):
    post= Posts.objects.filter(author=request.user)

# pagination
    page = request.GET.get('page')
    paginator = Paginator(post,3)
    try:
        post = paginator.page(page)
    except PageNotAnInteger:
        page = 1
        post = paginator.page(page)
    except EmptyPage:
        page = paginator.num_pages
        post = paginator.page(page)

# End paginator
     
    if request.method=='POST':
        user_form=UserUpdateForm(request.POST,instance=request.user)
        profile_form=ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        if user_form.is_valid and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request,'update successful')
            return redirect('profile')
    else:
        user_form=UserUpdateForm(instance=request.user)
        profile_form=ProfileUpdateForm(instance=request.user.profile)
    context={'user_form':user_form, 'profile_form':profile_form, 'post':post, 'paginator': paginator} 
    return render( request, 'user/profile.html', context )
    
   
