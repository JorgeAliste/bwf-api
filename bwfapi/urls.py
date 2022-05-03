from django.urls import path, include, re_path

from bwfapi import views
from rest_framework import routers

router = routers.DefaultRouter()
router.register('groups', views.GroupViewSet)
router.register('events', views.EventViewSet)
router.register('users', views.UserViewSet)

urlpatterns = [
    re_path(r'^', include(router.urls)),
    path('authenticate/', views.CustomObtainAuthToken.as_view()),
]
