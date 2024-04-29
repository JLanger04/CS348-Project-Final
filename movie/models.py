from django.db import models

class Director(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    def __str__(self):
        return self.name

class Main_Actor(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    def __str__(self):
        return self.name

class Movies(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=255)
    release_year = models.PositiveIntegerField(default=0, db_index=True)
    duration = models.PositiveIntegerField(default=0)
    main_actor = models.ForeignKey(Main_Actor, on_delete=models.CASCADE, db_index=True)
    director = models.ForeignKey(Director, on_delete=models.CASCADE, db_index=True)
    def __str__(self):
        return self.title

class Ranked(models.Model):
    id = models.AutoField(primary_key=True)
    movie = models.ForeignKey(Movies, on_delete=models.CASCADE)
    rating = models.IntegerField(default=0, db_index=True)