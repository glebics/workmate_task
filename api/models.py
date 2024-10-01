# api/models.py
from django.db import models
from django.contrib.auth.models import User


class Breed(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class Kitten(models.Model):
    owner = models.ForeignKey(
        User, related_name='kittens', on_delete=models.CASCADE)
    breed = models.ForeignKey(
        Breed, related_name='kittens', on_delete=models.CASCADE)
    color = models.CharField(max_length=50)
    age = models.PositiveIntegerField(help_text="Возраст в полных месяцах")
    description = models.TextField()

    def __str__(self):
        return f"{self.breed.name} - {self.color} - {self.age} мес."


class Rating(models.Model):
    user = models.ForeignKey(
        User, related_name='ratings', on_delete=models.CASCADE)
    kitten = models.ForeignKey(
        Kitten, related_name='ratings', on_delete=models.CASCADE)
    score = models.PositiveSmallIntegerField()

    class Meta:
        unique_together = ('user', 'kitten')

    def __str__(self):
        return f"{self.user.username} оценил {self.kitten.id} на {self.score}"
