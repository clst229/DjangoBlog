from django import template
from django.utils import timezone
from ..models import Category,Post
from django.db.models import Count
from django.db.models.functions import TruncMonth

register = template.Library()

@register.inclusion_tag('thread/tags/category_list.html')
def render_category_links():
	return{
	'category_list': Category.objects.filter(post__is_public=True).annotate(post_count=Count('post')).order_by('id')
	}

@register.inclusion_tag('thread/tags/month_list.html')
def render_month_links(): 
	return{
	'month_list':Post.objects.filter(is_public=True).annotate(month=TruncMonth('created_date')).values('month').annotate(count=Count('pk')).order_by('month')
	}
