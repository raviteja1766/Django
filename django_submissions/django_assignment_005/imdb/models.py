from __future__ import unicode_literals

from django.db import models


class Actor(models.Model):
    actor_id = models.CharField(max_length=100, primary_key=True)
    name = models.CharField(max_length=100)
    gender = models.CharField(max_length=50, null=True)

    def __str__(self):
        return self.name


class Director(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class Movie(models.Model):
    movie_id = models.CharField(max_length=100, primary_key=True)
    name = models.CharField(max_length=100)
    actors = models.ManyToManyField(Actor, through='Cast')
    director = models.ForeignKey(Director, on_delete=models.CASCADE)
    release_date = models.DateField()
    box_office_collection_in_crores = models.FloatField()

    def __str__(self):
        return self.name


class Cast(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    actor = models.ForeignKey(Actor, on_delete=models.CASCADE)
    role = models.CharField(max_length=50)
    is_debut_movie = models.BooleanField(default=False)

    def __str__(self):
        return '{}@{}@{}'.format(self.actor_id,self.role,self.movie_id)


class Rating(models.Model):
    movie = models.OneToOneField(Movie, on_delete=models.CASCADE)
    rating_one_count = models.IntegerField(default=0)
    rating_two_count = models.IntegerField(default=0)
    rating_three_count = models.IntegerField(default=0)
    rating_four_count = models.IntegerField(default=0)
    rating_five_count = models.IntegerField(default=0)

    def __str__(self):
        return "Rating {}".format(self.id)