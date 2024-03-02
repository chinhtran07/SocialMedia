from django.urls import path, include, re_path
from rest_framework import routers
from . import views

router = routers.DefaultRouter()
router.register('users', views.UserViewSet, basename='users')
router.register('posts', views.PostViewSet, basename='posts')
router.register('comments', views.CommentViewSet, basename='comments')
router.register('friendship', views.FriendShipViewSet, basename='friendship')
router.register('groups', views.GroupViewSet, basename='groups')
router.register('surveys', views.SurveyViewSet, basename='surveys')
router.register('invitations', views.InvitationViewSet, basename='invitations')
router.register('notifications', views.NotificationViewSet, basename='notifications')
router.register('messages', views.MessageViewSet, basename='messages')

urlpatterns = [
    path('', include(router.urls)),
    path('login/', views.LoginView.as_view(), name='login'),
    path('register/', views.RegisterView.as_view(), name='register'),
    path('accounts/google/login/callback', views.google_callback, name="google_callback")
]
