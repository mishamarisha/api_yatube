from django.urls import include, path

from rest_framework.routers import DefaultRouter
from rest_framework.authtoken import views

from .views import PostViewSet, GroupViewSet, CommentList, CommentDetail

router = DefaultRouter()
router.register(r'posts', PostViewSet, basename='posts')
router.register(r'groups', GroupViewSet, basename='groups')

urlpatterns = [
    path('api-token-auth/', views.obtain_auth_token),
    path('', include(router.urls)),
    path(
        'posts/<int:post_id>/comments/',
        CommentList.as_view(),
        name='comment_list'
    ),
    path(
        'posts/<int:post_id>/comments/<int:pk>/',
        CommentDetail.as_view(),
        name='comment_detail'
    ),
]
