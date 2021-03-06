from django.conf import settings
from django.core.validators import MaxLengthValidator, MinLengthValidator
from django.db import models
from django.utils import timezone

class Category(models.Model):
    name = models.CharField(max_length=15,
                            validators=[MaxLengthValidator(15,'15文字以内で入力してください')],
                            unique=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


def set_default_category():
    category = Category.objects.get_or_create(name='未設定')
    return category

class PostManager(models.Manager):
    def published(self):
        self.get_queryset().filter(is_public=True,created_date__lte=timezone.now()).order_by('created_date').reverse()

class Post(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=30,
                             validators=[MaxLengthValidator(30,'30文字以内で入力してください')])
    category = models.ForeignKey(Category,on_delete=models.SET_DEFAULT,default=set_default_category)
    text = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)
    updated_date = models.DateTimeField(blank=True, null=True)
    is_public = models.BooleanField(default=False)

    objects = PostManager()

    def publish(self):
        self.is_public = True
        self.save()

    def __str__(self):
        return self.title
    
    def approved_comments(self):
        return self.comments.filter(approved_comment=True)
    
    def count_unnapproved_comment(self):
        return self.comments.filter(approved_comment=False).count()


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

