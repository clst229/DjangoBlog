from django.shortcuts import render, get_object_or_404,redirect
from django.utils import timezone
from .models import Post,Comment,Category,Tag
from .forms import PostForm,CommentForm
from django.contrib.auth.decorators import login_required
from django.views import generic
from django.views.generic import ListView,DetailView
from django.views.generic.dates import YearArchiveView

from django.db.models import Q

from functools import reduce
from operator import and_

# Create your views here.
#def post_list(request):
#    posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date').reverse()
#    return render(request, 'blog/post_list.html', {'posts':posts})

class Post_List(ListView):
    model = Post
    paginate_by = 5
    context_object_name = 'posts'
    template_name = 'blog/post_list.html'

    def get_queryset(self):
        queryset = Post.objects.filter(is_public=True,created_date__lte=timezone.now()).order_by('created_date').reverse()
        q_word = self.request.GET.get('query')
        if q_word:
            exclusion = set([' ','　'])
            q_list = ''
            for i in q_word:
                if i in exclusion:
                    pass
                else:
                    q_list += i
            query = reduce(
                and_,[Q(title__icontains=q)|Q(text__icontains=q) for q in q_list]
                )
            object_list = queryset.filter(query)
        else:
            object_list =Post.objects.filter(is_public=True,created_date__lte=timezone.now()).order_by('created_date').reverse()
        return object_list

#def post_detail(request, pk):
#    post = get_object_or_404(Post,pk=pk)
#    return render(request,'blog/post_detail.html',{'post':post})

class Post_Detail(DetailView):
    template_name = 'blog/post_detail.html'
    model = Post

@login_required
def post_new(request):
    if request.method == "POST":
        form= PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            if 'publish' in request.POST:
                post.updated_date = timezone.now()
                post.is_public = True
            elif 'draft' in request.POST:
                post.is_public = False
            post.save()
            return redirect('post_detail',pk=post.pk)
    else:
        form = PostForm()
    return render(request,'blog/post_edit.html',{'form':form})

@login_required
def post_edit(request,pk) :
    post = get_object_or_404(Post,pk=pk)
    if request.method == "POST":
        form = PostForm(request.POST,instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            if 'publish' in request.POST:
                post.updated_date = timezone.now()
                post.is_public = True
            elif 'draft' in request.POST:
                post.is_public = False
            post.save()
            return redirect('post_detail',pk=post.pk)
    else:
        form = PostForm(instance=post)
    return render(request,'blog/post_edit.html',{'form':form})

@login_required
def post_draft_list(request):
    posts = Post.objects.filter(is_public = False).order_by('created_date')
    return render(request,'blog/post_draft_list.html',{'posts':posts})

@login_required
def post_publish(request,pk):
    post = get_object_or_404(Post,pk=pk)
    post.publish()
    return redirect('post_detail', pk=pk)

@login_required
def post_remove(request,pk):
    post = get_object_or_404(Post,pk=pk)
    post.delete()
    return redirect('post_list')


def add_comment_to_post(request,pk):
    post = get_object_or_404(Post,pk=pk)
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.save()
            return redirect('post_detail',pk=post.pk)
    else:
        form = CommentForm()
    return render(request, 'blog/add_comment_to_post.html',{'form':form})

@login_required
def comment_approve(request,pk):
    comment = get_object_or_404(Comment,pk=pk)
    comment.approve()
    return redirect('post_detail',pk=comment.post.pk)

@login_required
def comment_remove(request,pk):
    comment = get_object_or_404(Comment,pk=pk)
    comment.delete()
    return redirect('post_detail',pk=comment.post.pk)

def category_list(request,pk):
    category = get_object_or_404(Category,pk=pk)
    posts =  Post.objects.filter(category=category,created_date__lte=timezone.now(),is_public=True).order_by('created_date').reverse()
    return render(request, 'blog/post_list.html', {'posts':posts}) 

#class Category_List(ListView):
#    model = Category
#    paginate_by = 5
#    context_object_name = 'posts'
#    templete_name = 'blog/post_list.html'

class Post_Year_Archive_List(ListView):
    model = Post
    paginate_by = 5
    context_object_name = 'posts'
    template_name = 'blog/post_list.html'

    def get_queryset(self):
        return Post.objects.filter(created_date__lte=timezone.now()).order_by('created_date').reverse()
