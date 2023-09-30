from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PostView, Job_levelView, Job_typeView

router = DefaultRouter()
router.register('posts', PostView)
router.register('level', Job_levelView)
router.register('type', Job_typeView)


urlpatterns = [
    path('', include(router.urls)),
]