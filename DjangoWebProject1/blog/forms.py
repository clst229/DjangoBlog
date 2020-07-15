from django import forms

from .models import Post,Comment,Category,Tag

class PostForm(forms.ModelForm):
	
	class Meta:
		model = Post
		fields = ('title','category','tags','text',)

class CommentForm(forms.ModelForm):

	class Meta:
		model = Comment
		fields = ('author','text',)

