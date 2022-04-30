from django.urls import path, include, re_path

from bwfapi import views
from rest_framework import routers

router = routers.DefaultRouter()
router.register('groups', views.GroupViewset)

urlpatterns = [
    re_path(r'^', include(router.urls))
]
