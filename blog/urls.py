from django.urls import path, include
from . import views

urlpatterns = [
#    path('', views.index),
    path('', views.PostList.as_view()),
    path('<int:pk>/', views.PostDetail.as_view()),
    path('<int:pk>/update/', views.PostUpdate.as_view()),
    path('<int:pk>/new_comment/', views.new_comment),
    path('delete_comment/<int:pk>/', views.delete_comment),
    path('create/', views.PostCreate.as_view()),
    path('accounts/', include('allauth.urls')),
    path('search/<str:q>/', views.PostSearch.as_view())
]
