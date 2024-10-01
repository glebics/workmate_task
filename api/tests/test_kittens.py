import pytest
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from django.contrib.auth.models import User
from api.models import Breed, Kitten, Rating
from rest_framework_simplejwt.tokens import RefreshToken


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def create_user():
    return User.objects.create_user(username='testuser', password='testpass')


@pytest.fixture
def create_another_user():
    return User.objects.create_user(username='anotheruser', password='anotherpass')


@pytest.fixture
def create_breed():
    return Breed.objects.create(name='Siamese')


@pytest.fixture
def create_kitten(create_user, create_breed):
    return Kitten.objects.create(
        owner=create_user,
        breed=create_breed,
        color='Blue',
        age=3,
        description='A cute Siamese kitten.'
    )


@pytest.fixture
def create_rating(create_user, create_kitten):
    return Rating.objects.create(
        user=create_user,
        kitten=create_kitten,
        score=4
    )


# Helper function to authenticate user and get JWT token
def authenticate_user(client, user):
    refresh = RefreshToken.for_user(user)
    client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')


# Тесты для Breed (Породы)

@pytest.mark.django_db
def test_get_breeds(api_client, create_breed):
    url = reverse('breed-list')
    response = api_client.get(url)
    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) == 1
    assert response.data[0]['name'] == 'Siamese'


# Тесты для Kitten (Котята)

@pytest.mark.django_db
def test_get_kittens(api_client, create_kitten):
    url = reverse('kitten-list')
    response = api_client.get(url)
    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) == 1
    assert response.data[0]['color'] == 'Blue'


@pytest.mark.django_db
def test_create_kitten(api_client, create_user, create_breed):
    url = reverse('kitten-list')
    authenticate_user(api_client, create_user)
    data = {
        "breed_id": create_breed.id,
        "color": "White",
        "age": 2,
        "description": "A playful kitten."
    }
    response = api_client.post(url, data, format='json')
    assert response.status_code == status.HTTP_201_CREATED
    assert Kitten.objects.count() == 1
    assert Kitten.objects.get().color == 'White'


@pytest.mark.django_db
def test_update_kitten(api_client, create_user, create_kitten):
    url = reverse('kitten-detail', args=[create_kitten.id])
    authenticate_user(api_client, create_user)
    data = {
        "breed_id": create_kitten.breed.id,
        "color": "Green",
        "age": 4,
        "description": "Updated description"
    }
    response = api_client.put(url, data, format='json')
    assert response.status_code == status.HTTP_200_OK
    create_kitten.refresh_from_db()
    assert create_kitten.color == 'Green'
    assert create_kitten.age == 4
    assert create_kitten.description == 'Updated description'


@pytest.mark.django_db
def test_delete_kitten(api_client, create_user, create_kitten):
    url = reverse('kitten-detail', args=[create_kitten.id])
    authenticate_user(api_client, create_user)
    response = api_client.delete(url)
    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert Kitten.objects.count() == 0


# Тесты для Rating (Оценки котят)


@pytest.mark.django_db
def test_create_rating(api_client, create_user, create_kitten):
    url = reverse('rating-list')
    authenticate_user(api_client, create_user)

    # Передаем корректный ID котенка
    data = {
        "kitten": create_kitten.id,
        "score": 5
    }
    response = api_client.post(url, data, format='json')

    # Проверяем статус и создание рейтинга
    assert response.status_code == status.HTTP_201_CREATED
    assert Rating.objects.count() == 1
    assert Rating.objects.get().score == 5
    assert Rating.objects.get().kitten == create_kitten


@pytest.mark.django_db
@pytest.mark.django_db
def test_get_ratings(api_client, create_user, create_rating):
    url = reverse('rating-list')
    authenticate_user(api_client, create_user)  # Аутентификация пользователя
    response = api_client.get(url)

    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) == 1
    assert response.data[0]['score'] == 4


# Тестирование прав на действия с котёнком

@pytest.mark.django_db
def test_update_kitten_not_owner(api_client, create_another_user, create_kitten):
    url = reverse('kitten-detail', args=[create_kitten.id])
    authenticate_user(api_client, create_another_user)
    data = {
        "breed_id": create_kitten.breed.id,
        "color": "Yellow",
        "age": 6,
        "description": "Trying to update as not owner"
    }
    response = api_client.put(url, data, format='json')
    assert response.status_code == status.HTTP_403_FORBIDDEN
