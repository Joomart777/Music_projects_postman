from django.contrib import admin

# Register your models here.
#from music_app.models import Category
from music_app.models import *

admin.site.register(Category)
admin.site.register(Music)
