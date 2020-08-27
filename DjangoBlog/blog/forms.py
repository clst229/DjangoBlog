from django import forms

from .models import Post,Comment,Category
class PostForm(forms.ModelForm):
	
	class Meta:
		model = Post
		fields = ('title','category','text',)
		error_messages ={
			'title' :{
				'max_length':'30文字以内で入力してください'
				}
			}

class CommentForm(forms.ModelForm):

	class Meta:
		model = Comment
		fields = ('author','text',)

