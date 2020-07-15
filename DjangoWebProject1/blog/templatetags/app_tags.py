from django import template
from django.utils import timezone
from ..models import Category,Post
from django.db.models import Count

register = template.Library()

@register.inclusion_tag('thread/tags/category_list.html')
def render_category_links():
	return{
	'category_list': Category.objects.annotate(post_count=Count('post'))
	}

@register.inclusion_tag('thread/tags/month_list.html')
def render_month_links():
	return{
	'month_list': Post.objects.filter(published_date__lte=timezone.now()).dates('published_date', 'month', order='DESC'),
	}