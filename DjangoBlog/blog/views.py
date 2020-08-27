from django.shortcuts import render, get_object_or_404,redirect
from django.utils import timezone
from .models import Post,Comment,Category
from .forms import PostForm,CommentForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import generic
from django.views.generic import ListView,DetailView,CreateView,UpdateView
from django.urls import reverse_lazy
from django.views.generic.dates import MonthArchiveView
from django.db.models import Q
from functools import reduce
from operator import and_

#記事一覧（Function-Based Views）
#def post_list(request):
#    posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date').reverse()
#    return render(request, 'blog/post_list.html', {'posts':posts})

#記事一覧（Class-Based Views）
class Post_List(ListView):
    model = Post
    paginate_by = 5
    #context_object_name = 'posts'
    template_name = 'blog/post_list.html'

    def get_queryset(self):
        return Post.objects.filter(is_public=True,created_date__lte=timezone.now()).order_by('created_date').reverse()

#記事詳細（Function-Based Views）
#def post_detail(request, pk):
#    post = get_object_or_404(Post,pk=pk)
#    return render(request,'blog/post_detail.html',{'post':post})

#記事詳細（Class-Based Views）
class Post_Detail(DetailView):
    template_name = 'blog/post_detail.html'
    model = Post

#記事検索
class Search_List(ListView):
    model = Post
    template_name = 'blog/post_list.html'
    paginate_by = 5

    def get_queryset(self):
        queryset = Post.objects.filter(is_public=True,created_date__lte=timezone.now()).order_by('created_date').reverse()
        object_list = queryset
        q_word = self.request.GET.get('query','')
        if q_word:
            q_list = q_word.replace(' ','　').split()
            if q_list:
                query = reduce(
                    and_,[Q(title__icontains=q)|Q(text__icontains=q) for q in q_list]
                    )
                object_list = queryset.filter(query)
            
        return object_list

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        query = self.request.GET.get('query')
        if query:
            context['query'] = query
        return context


#記事作成（Function-Based Views）
#@login_required
#def post_new(request):
#    if request.method == "POST":
#        form= PostForm(request.POST)
#        if form.is_valid():
#            post = form.save(commit=False)
#            post.author = request.user
#            if 'publish' in request.POST:
#                post.updated_date = timezone.now()
#                post.is_public = True
#            elif 'draft' in request.POST:
#                post.is_public = False
#            post.save()
#            return redirect('post_detail',pk=post.pk)
#    else:
#        form = PostForm()
#    return render(request,'blog/post_edit.html',{'form':form})

#記事作成（Class-Based Views）
class Post_New(LoginRequiredMixin,CreateView):
    form_class = PostForm
    template_name = 'blog/post_edit.html'

    def post(self, request, *args, **kwargs):
        form= PostForm(request.POST)
        return super().post(request, *args, **kwargs)

    def form_valid(self, form):
      post = form.save(commit=False)
      post.author = self.request.user
      if 'publish' in self.request.POST:
         post.updated_date = timezone.now()
         post.is_public = True
      elif 'draft' in self.request.POST:
         post.is_public = False
         post.save()
      return super().form_valid(form)
    
    def get_success_url(self):
      return reverse_lazy('post_detail',kwargs={'pk':self.object.id})

#記事編集（Function-Based Views）
#@login_required
#def post_edit(request,pk) :
#    post = get_object_or_404(Post,pk=pk)
#    if request.method == "POST":
#        form = PostForm(request.POST,instance=post)
#        if form.is_valid():
#            post = form.save(commit=False)
#            post.author = request.user
#            if 'publish' in request.POST:
#                post.updated_date = timezone.now()
#                post.is_public = True
#            elif 'draft' in request.POST:
#                post.is_public = False
#            post.save()
#            return redirect('post_detail',pk=post.pk)
#    else:
#        form = PostForm(instance=post)
#    return render(request,'blog/post_edit.html',{'form':form})

#記事編集（Class-Based Views）
class Post_Edit(LoginRequiredMixin,UpdateView):
    form_class = PostForm
    template_name = 'blog/post_edit.html'
    model = Post

    def post(self, request, *args, **kwargs):
        form = PostForm(request.POST,instance=post)
        return super().post(request, *args, **kwargs)

    def form_valid(self, form):
         post = form.save(commit=False)
         post.author = self.request.user
         if 'publish' in self.request.POST:
             post.updated_date = timezone.now()
             post.is_public = True
         elif 'draft' in self.request.POST:
             post.is_public = False
         post.save()
         return super().form_valid(form)

    def get_success_url(self):
      return reverse_lazy('post_detail',kwargs={'pk':self.object.id})


#下書き一覧（Function-Based Views）
#@login_required
#def post_draft_list(request):
#    posts = Post.objects.filter(is_public = False).order_by('created_date').reverse
#    return render(request,'blog/post_draft_list.html',{'posts':posts})

#下書き一覧（Class-Based Views）
class Post_Draft_List(LoginRequiredMixin,ListView):
    model = Post
    template_name = 'blog/post_draft_list.html'
    paginate_by = 5

    def get_queryset(self):
        return Post.objects.filter(is_public = False).order_by('created_date').reverse()

#記事公開
@login_required
def post_publish(request,pk):
    post = get_object_or_404(Post,pk=pk)
    post.publish()
    return redirect('post_detail', pk=pk)

#記事削除
@login_required
def post_remove(request,pk):
    post = get_object_or_404(Post,pk=pk)
    post.delete()
    return redirect('post_list')

#コメント追加（Function-Based Views）
#def add_comment_to_post(request,pk):
#    post = get_object_or_404(Post,pk=pk)
#    if request.method == "POST":
#        form = CommentForm(request.POST)
#        if form.is_valid():
#            comment = form.save(commit=False)
#            comment.post = post
#            comment.save()
#            return redirect('post_detail',pk=post.pk)
#    else:
#        form = CommentForm()
#    return render(request, 'blog/add_comment_to_post.html',{'form':form})

#コメント追加（Class-Based Views）
class Add_Comment_To_Post(CreateView):
    model = Comment
    form_class = CommentForm
    template_name = 'blog/add_comment_to_post.html'

    def form_valid(self, form):
      post = get_object_or_404(Post,pk=self.kwargs.get('pk'))
      comment = form.save(commit=False)
      comment.post = post
      comment.save()
      return super().form_valid(form)
    
    def get_success_url(self):
      return reverse_lazy('post_detail',kwargs={'pk': self.kwargs.get('pk')})

#コメント承認
@login_required
def comment_approve(request,pk):
    comment = get_object_or_404(Comment,pk=pk)
    comment.approve()
    return redirect('post_detail',pk=comment.post.pk)

#コメント削除（否決）
@login_required
def comment_remove(request,pk):
    comment = get_object_or_404(Comment,pk=pk)
    comment.delete()
    return redirect('post_detail',pk=comment.post.pk)

#カテゴリ別一覧（Function-Based Views）
#def category_list(request,pk):
#    category = get_object_or_404(Category,pk=pk)
#    posts =  Post.objects.filter(category=category,created_date__lte=timezone.now(),is_public=True).order_by('created_date').reverse()
#    return render(request, 'blog/post_list.html', {'posts':posts}) 

#カテゴリ別一覧（Class-Based Views）
class Category_List(ListView):
    model = Post
    paginate_by = 5
    #context_object_name = 'posts'
    templete_name = 'blog/post_list.html'

    def get_queryset(self):
        pk = self.kwargs.get('pk')
        category = get_object_or_404(Category,pk=pk)
        return Post.objects.filter(category=category,created_date__lte=timezone.now(),is_public=True).order_by('created_date').reverse()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        pk = self.kwargs.get('pk')
        category = get_object_or_404(Category,pk=pk)
        context['category_name'] = str(category)
        return context

#カテゴリ作成
class CategoryCreate(CreateView):
    model = Category
    fields = ['name']
    template_name = 'blog/category_form.html'
    
    def get_success_url(self):
        path = request.path
        if "edit" in path:
            return reverse('post_edit',kwargs={'pk':self.object.pk})
        else:
            return reverse('post_new')

#カテゴリ作成（ポップアップ用）
class PopupCategoryCreate(CategoryCreate):

    def form_valid(self,form):
        category = form.save()
        context = {
            'object_name':str(category),
            'object_pk':category.pk,
            'function_name':'add_category'
            }
        return render(self.request,'blog/close.html',context)

##年別記事一覧
#class Post_Year_Archive_List(ListView):
#    model = Post
#    #context_object_name = 'posts'
#    template_name = 'blog/post_list.html'

#    def get_queryset(self):
#        return Post.objects.filter(created_date__lte=timezone.now()).order_by('created_date').reverse()

#月別記事一覧
class Post_Month_Archive_View(MonthArchiveView):
    queryset =Post.objects.all()
    paginate_by = 5
    date_field = "created_date"
    template_name = 'blog/post_list.html'

    def get_queryset(self):
        return super().get_queryset().filter(is_public=True,created_date__lte=timezone.now()).order_by('created_date').reverse()

