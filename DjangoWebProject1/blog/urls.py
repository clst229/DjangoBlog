from django.urls import path
from . import views


urlpatterns = [
    path('', views.Post_List.as_view(), name='post_list'),
    path('post/<int:pk>/',views.Post_Detail.as_view(),name='post_detail'),
    path('post/new/',views.post_new,name='post_new'),
    path('post/<int:pk>/edit', views.post_edit , name='post_edit'),
    path('drafts/',views.post_draft_list,name='post_draft_list'),
    path('post/<int:pk>/publish',views.post_publish,name='post_publish'),
    path('post/<int:pk>/remove/',views.post_remove,name='post_remove'),
    path('post/<int:pk>/comment/',views.add_comment_to_post,name='add_comment_to_post'),
    path('comment/<int:pk>/approve',views.comment_approve,name='comment_approve'),
    path('comment/<int:pk>/remove',views.comment_remove,name='comment_remove'),
    path('category/<int:pk>/',views.Category_List.as_view(),name='category_list'),
    path('category_create/',views.PopupCategoryCreate.as_view(),name='category_create'),
    path('year/<int:year>/',views.Post_Year_Archive_List.as_view(),name='month_list'),
    path('<int:year>/<int:month>/',views.PostMonthArchiveView.as_view(month_format='%m'),name="archive_month"),
    path('search_result/',views.Search_List.as_view(),name='search_list'),
    ]
