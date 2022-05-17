from django.urls import path, include, re_path

from bwfapi import views
from rest_framework import routers

router = routers.DefaultRouter()
router.register('groups', views.GroupViewSet)
router.register('events', views.EventViewSet)
router.register('members', views.MemberViewSet)
router.register('comments', views.CommentViewSet)
router.register('bets', views.BetViewSet)
router.register('users', views.UserViewSet)
router.register('profiles', views.UserProfileViewSet)

urlpatterns = [
    re_path(r'^', include(router.urls)),
    path('authenticate/', views.CustomObtainAuthToken.as_view()),
]
