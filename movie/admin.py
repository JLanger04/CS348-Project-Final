from django.contrib import admin

# Register your models here.
from .models import Movies, Main_Actor, Director, Ranked
# Register your models here
admin.site.register(Movies)
admin.site.register(Main_Actor)
admin.site.register(Director)
admin.site.register(Ranked)