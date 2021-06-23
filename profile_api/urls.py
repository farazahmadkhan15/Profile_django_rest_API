from django.urls import path, include

from rest_framework.routers import DefaultRouter
from profile_api import views

router = DefaultRouter()
router.register('hello-viewset', views.HelloViewSet, basename="hello-viewSet")

urlpatterns = [
    path('hello-view/' ,views.HelloApiView.as_view()),
    path('',include(router.urls))
]
