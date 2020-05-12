from imdb.models import *
from django.db.models import *
from django.db import *


def populate_database(actors_list, movies_list, directors_list, movie_rating_list):

    Actor.objects.bulk_create([Actor(
                actor_id = actor['actor_id'],
                name = actor['name']
            )for actor in actors_list])
        
    Director.objects.bulk_create(
        [ Director(name=director) for director in directors_list ]
    )
    
    movie_list = []    
    cast_list = []
    director_objs = Director.objects.all()
    for movie in movies_list:
        for director in director_objs:
            if director.name == movie['director_name']:
                director_obj = director
                break
        movie_list.append(
            Movie(movie_id = movie['movie_id'],
                name = movie['name'],
                box_office_collection_in_crores = movie['box_office_collection_in_crores'],
                release_date = movie['release_date'],
                director = director_obj
            )
        )
        for actor in movie['actors']:
            cast_list.append(
                Cast(
                    actor_id = actor['actor_id'],
                    movie_id = movie['movie_id'],
                    role = actor['role'],
                    is_debut_movie = actor['is_debut_movie']
                )
            )
    Movie.objects.bulk_create(movie_list)
    
    Cast.objects.bulk_create(cast_list)
    
    Rating.objects.bulk_create([
        Rating(
                movie_id = movie_rate['movie_id'],
                rating_one_count = movie_rate['rating_one_count'],
                rating_two_count = movie_rate['rating_two_count'],
                rating_three_count = movie_rate['rating_three_count'],
                rating_four_count = movie_rate['rating_four_count'],
                rating_five_count = movie_rate['rating_five_count']
            ) for movie_rate in movie_rating_list
    ])

def get_average_rating_of_movie(movie_obj):
    
    try:
        rate_obj = movie_obj.rating
        one = rate_obj.rating_one_count 
        two = rate_obj.rating_two_count 
        three = rate_obj.rating_three_count 
        four = rate_obj.rating_four_count  
        five = rate_obj.rating_five_count 
        sum_of_ratings = one + two * 2 + three * 3 + four * 4 + five * 5
        no_of_ratings = one + two + three + four + five
        return sum_of_ratings/no_of_ratings
    except ZeroDivisionError:
        return 0
    except Rating.DoesNotExist:
        return 0

def total_number_of_ratings(movie_obj):
    
    try:
        rate_obj = movie_obj.rating
        sum_of_ratings = (rate_obj.rating_one_count 
            + rate_obj.rating_two_count
            + rate_obj.rating_three_count
            + rate_obj.rating_four_count  
            + rate_obj.rating_five_count)
        return sum_of_ratings
    except Rating.DoesNotExist:
        return 0

def get_movies_by_given_cast_objects(cast_objs):
    movie_lst = []
    movie_list=[]
    for cast in cast_objs:
        if cast.movie not in movie_lst:
            cast_list = []
            movie_lst.append(cast.movie)
            movie_obj = cast.movie
            movie_list.append({
                'movie_id': movie_obj.movie_id,
                'name': movie_obj.name,
                'cast': cast_list,
                'box_office_collection_in_crores': movie_obj.box_office_collection_in_crores,
                'release_date': str(movie_obj.release_date),
                'director_name': movie_obj.director.name,
                'average_rating': get_average_rating_of_movie(movie_obj),
                'total_number_of_ratings': total_number_of_ratings(movie_obj)
            })
        cast_list.append({
        'actor':{
                    'name': cast.actor.name,
                    'actor_id': cast.actor_id
                },
        'role': cast.role,
        'is_debut_movie': cast.is_debut_movie
        })
    return movie_list

def get_movies_by_given_movie_names(movie_names):
    cast_objs = Cast.objects.filter(
                    movie__name__in=movie_names).select_related(
                        'movie__director','movie__rating','actor')
    return get_movies_by_given_cast_objects(cast_objs)

def get_movies_released_in_summer_in_given_years():
    cast_objs = Cast.objects.filter(movie__in = Movie.objects.filter(
        release_date__month__range=(5,7),
        release_date__year__range=(2006,2009)
    ).distinct()).select_related(
                        'movie__director','movie__rating','actor')
    return get_movies_by_given_cast_objects(cast_objs)

def get_movie_names_with_actor_name_ending_with_smith():
    return list(Movie.objects.values_list('name',flat = True).filter(
                    actors__name__iendswith='smith').distinct())

def get_movie_names_with_ratings_in_given_range():
    return list(Movie.objects.filter(
                rating__rating_five_count__range=(1000,3000)
                ).values_list('name',flat = True).distinct())            

def get_movie_names_with_ratings_above_given_minimum():
    return list(Movie.objects.values_list('name',flat = True).filter(
        Q(release_date__year__range=(2001,2100)),
        Q(rating__rating_five_count__gte=500) | 
        Q(rating__rating_four_count__gte=1000) |
        Q(rating__rating_three_count__gte=2000) | 
        Q(rating__rating_two_count__gte=4000) |
        Q(rating__rating_one_count__gte=8000)
        ).distinct())

def get_movie_directors_in_given_year():
    return list(Director.objects.values_list('name',flat = True).filter(
        movie__release_date__year=2000).distinct())

def get_actor_names_debuted_in_21st_century():
    return list(Cast.objects.values_list('actor__name',flat=True).filter(
        movie__release_date__year__range=(2001,2100),is_debut_movie=True).distinct())
    
def get_director_names_containing_big_as_well_as_movie_in_may():
    return list(Director.objects.values_list(
                        'name',flat = True).filter(
                            movie__name__contains='big').filter(
                                movie__release_date__month=5).distinct())

def get_director_names_containing_big_and_movie_in_may():
    return list(Director.objects.values_list(
                        'name',flat = True).filter(
                            movie__name__contains='big',
                                movie__release_date__month=5).distinct())

def reset_ratings_for_movies_in_this_year():
    Rating.objects.filter(movie__release_date__year=2000).update(
        rating_one_count = 0,
        rating_two_count = 0,
        rating_three_count = 0,
        rating_four_count = 0,
        rating_five_count = 0)
    