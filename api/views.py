# api/views.py

from rest_framework import viewsets, permissions, filters
from .models import Breed, Kitten, Rating
from .serializers import BreedSerializer, KittenSerializer, KittenCreateUpdateSerializer, RatingSerializer
from .permissions import IsOwnerOrReadOnly
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import UserRegisterSerializer
from rest_framework import status


class BreedViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint для просмотра пород.
    """
    queryset = Breed.objects.all()
    serializer_class = BreedSerializer


class KittenViewSet(viewsets.ModelViewSet):
    """
    API endpoint для управления котятами.
    """
    queryset = Kitten.objects.all()
    serializer_class = KittenSerializer
    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
    filter_backends = [filters.SearchFilter]
    search_fields = ['breed__name']

    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return KittenCreateUpdateSerializer
        return KittenSerializer

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    @action(detail=False, methods=['get'], url_path='breed/(?P<breed_name>[^/.]+)')
    def kittens_by_breed(self, request, breed_name=None):
        """
        Получение котят по определённой породе.
        """
        kittens = self.queryset.filter(breed__name__iexact=breed_name)
        page = self.paginate_queryset(kittens)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(kittens, many=True)
        return Response(serializer.data)


class RatingViewSet(viewsets.ModelViewSet):
    """
    API endpoint для управления оценками котят.
    """
    queryset = Rating.objects.all()
    serializer_class = RatingSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class UserRegisterView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = UserRegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
