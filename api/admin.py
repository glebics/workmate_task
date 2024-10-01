# api/admin.py

from django.contrib import admin
from .models import Breed, Kitten, Rating

admin.site.register(Breed)
admin.site.register(Kitten)
admin.site.register(Rating)
