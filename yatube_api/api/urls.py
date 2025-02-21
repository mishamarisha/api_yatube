from django.urls import include, path

from rest_framework.routers import DefaultRouter
from rest_framework.authtoken import views

from .views import PostViewSet, GroupViewSet, CommentList, CommentDetail

API_VERSION_1 = 'v1'

router = DefaultRouter()
router.register('posts', PostViewSet, basename='v1-posts')
router.register('groups', GroupViewSet, basename='v1-groups')

urlpatterns = [
    path(f'{API_VERSION_1}/api-token-auth/', views.obtain_auth_token),
    path(f'{API_VERSION_1}/', include(router.urls)),
    path(
        f'{API_VERSION_1}/posts/<int:post_id>/comments/',
        CommentList.as_view(),
        name='comment_list'
    ),
    path(
        f'{API_VERSION_1}/posts/<int:post_id>/comments/<int:pk>/',
        CommentDetail.as_view(),
        name='comment_detail'
    ),
]
