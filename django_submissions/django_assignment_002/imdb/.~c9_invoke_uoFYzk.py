from django.db import models


class Director(models.Model):
    name = models.CharField(max_length = 200,unique=True)
    
class Movie(models.Model):
    name = models.CharField(max_length=100)
    movie_id = models.CharField(max_length=100,unique=True)
    release_date = models.DateField()
    box_office_collection_in_crores = models.FloatField()
    director = models.ForeignKey(Director,on_delete = models.CASCADE)

class Actor(models.Model):
    actor_id = models.CharField(max_length=100,unique=True)
    name = models.CharField(max_length = 100)

class Cast(models.Model):
    actor = models.ForeignKey(Actor,on_delete = models.CASCADE)
    movie = models.ForeignKey(Movie,on_delete = models.CASCADE)
    role = models.CharField(max_length = 50)
    is_debut_movie = models.BooleanField(default = False)
    
class Rating(models.Model):
    
    