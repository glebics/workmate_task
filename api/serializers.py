# api/serializers.py

from rest_framework import serializers
from .models import Breed, Kitten, Rating
from django.contrib.auth.models import User


class UserRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('username', 'password', 'email')

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password'],
            email=validated_data.get('email')
        )
        return user


class BreedSerializer(serializers.ModelSerializer):
    class Meta:
        model = Breed
        fields = ['id', 'name']


class KittenSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    breed = BreedSerializer(read_only=True)
    breed_id = serializers.PrimaryKeyRelatedField(
        queryset=Breed.objects.all(), source='breed', write_only=True)

    class Meta:
        model = Kitten
        fields = ['id', 'owner', 'breed', 'breed_id',
                  'color', 'age', 'description']


class KittenCreateUpdateSerializer(serializers.ModelSerializer):
    breed_id = serializers.PrimaryKeyRelatedField(
        queryset=Breed.objects.all(), source='breed')

    class Meta:
        model = Kitten
        fields = ['breed_id', 'color', 'age', 'description']


class RatingSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')
    kitten = serializers.PrimaryKeyRelatedField(queryset=Kitten.objects.all())

    class Meta:
        model = Rating
        fields = ['id', 'user', 'kitten', 'score']
