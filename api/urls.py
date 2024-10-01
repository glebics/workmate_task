# api/urls.py

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import BreedViewSet, KittenViewSet, RatingViewSet, UserRegisterView

router = DefaultRouter()
router.register(r'breeds', BreedViewSet)
router.register(r'kittens', KittenViewSet)
router.register(r'ratings', RatingViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('register/', UserRegisterView.as_view(),
         name='register'),
]
