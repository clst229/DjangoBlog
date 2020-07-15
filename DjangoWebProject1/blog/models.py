from django.conf import settings
from django.db import models
from django.utils import timezone

class Category(models.Model):
    name = models.CharField(max_length=30)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class Tag(models.Model):
    name = models.CharField(max_length=100)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
       return self.name


def set_default_category():
    category = Category.objects.get_or_create(name='未設定')
    return category

class PostManager(models.Manager):
    def published(self):
        self.get_queryset().filter(published_date__lte=timezone.now()).order_by('published_date').reverse()

class Post(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    category = models.ForeignKey(Category,on_delete=models.SET_DEFAULT,default=set_default_category)
    tags = models.ManyToManyField(Tag,blank=True)
    text = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)
    published_date = models.DateTimeField(blank=True, null=True)
    

    objects = PostManager()

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def __str__(self):
        return self.title
    
    def approved_comments(self):
        return self.comments.filter(approved_comment=True)


class Comment(models.Model):
    post = models.ForeignKey('blog.post',on_delete=models.CASCADE,related_name='comments')
    author = models.CharField(max_length=200)
    text = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)
    approved_comment = models.BooleanField(default=False)

    def approve(self):
        self.approved_comment = True
        self.save()

    def __str__(self):
        return self.text

