from django.shortcuts import render, redirect
from .models import Posts
from .forms import PostCreationForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required 
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.core.mail import send_mail


# Create your views here.

# posts=[
# 	{
# 		'title':'Nakamura Hikaru',
# 		'content':'First post',
# 		'date':'25 February 2020',
# 		'author':'Miracle',
# 	},
# 	{
# 		'title':'Magnus Carlsen',
# 		'content':'Second post',
# 		'date':'26 February 2020',
# 		'author':'Hikaru',
# 	}
# ]

def home(request):
	posts = Posts.objects.all()
	page = request.GET.get('page')
	paginator = Paginator(posts,3)
	try:
		posts = paginator.page(page)
	except PageNotAnInteger:
		page = 1
		posts = paginator.page(page)
	except EmptyPage:
		page = paginator.num_pages
		posts = paginator.page(page)

	print(posts.number)
	context = {'posts':posts, 'paginator':paginator }
	return render(request,'blog/index.html',context)

@login_required
def createpost(request):
	profile=request.user
	form=PostCreationForm()
	if request.method=='POST':
		form=PostCreationForm(request.POST,request.FILES)
		if form.is_valid():
			project=form.save(commit=False)
			project.author=profile
			project.save()	
			messages.success(request, 'post created successfully')
			return redirect('home')
	return render(request,'blog/createpost.html',{'form': form})

@login_required
def updatepost(request,pk):
	getpost = Posts.objects.get(id=pk)
	form = PostCreationForm(instance=getpost)
	post = Posts.objects.filter(id=pk)
	if request.method == 'POST':
		form = PostCreationForm(request.POST, request.FILES, instance=getpost)
		if form.is_valid():
			form.save()
			messages.success(request, 'post updated successfully')
			return redirect('home')
	context = {'post':post, 'form':form}
	return render(request,'blog/updatepost.html',context)

def deletepost(request, pk):
	if request.method == 'POST':
		post = Posts.objects.filter(id=pk)
		post.delete()
		messages.success(request, 'post deleted successfully')
		return redirect('home')
	return render(request, 'blog/deletepost.html')

def single(request, pk):
	post = Posts.objects.filter(id = pk)
	context = {'post':post}
	return render(request, 'blog/single.html', context)