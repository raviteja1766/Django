from imdb.models import *
from django.db.models import *
from django.db import *


actors_list = [
        {
            "actor_id": "actor_1",
            "name": "jason smith",
            "gender": "MALE"
        },
        {
            "actor_id": "actor_2",
            "name": "baba fakruddhin",
            "gender": "FEMALE"
        },
        {
            "actor_id": "actor_3",
            "name": "mahesh babu",
            "gender": "MALE"
        },
        {
            "actor_id": "actor_4",
            "name": "naveen kumar",
            "gender": "FEMALE"
        },
        {
            "actor_id": "actor_5",
            "name": "rav iteja",
            "gender": "MALE"
        }
]
movies_list =  [
        {
            "movie_id": "movie_1",
            "name": "Movie 1",
            "actors": [
                {
                    "actor_id": "actor_2",
                    "role": "hero",
                    "is_debut_movie": False
                },
                {
                    "actor_id": "actor_3",
                    "role": "villan",
                    "is_debut_movie": True
                },
                {
                    "actor_id": "actor_4",
                    "role": "comedian",
                    "is_debut_movie": True
                },
                {
                    "actor_id": "actor_5",
                    "role": "side character",
                    "is_debut_movie": True
                }
            ],
            "box_office_collection_in_crores": "12.3",
            "release_date": "2006-5-3",
            "director_name": "Director 1"
        },
        {
            "movie_id": "movie_2",
            "name": "Movie 2",
            "actors": [
                {
                    "actor_id": "actor_1",
                    "role": "hero",
                    "is_debut_movie": False
                },
                {
                    "actor_id": "actor_3",
                    "role": "villan",
                    "is_debut_movie": True
                },
                {
                    "actor_id": "actor_4",
                    "role": "comedian",
                    "is_debut_movie": True
                },
                {
                    "actor_id": "actor_5",
                    "role": "side character",
                    "is_debut_movie": True
                }
            ],
            "box_office_collection_in_crores": "15.3",
            "release_date": "2000-5-3",
            "director_name": "Director 1"
        },
        {
            "movie_id": "movie_3",
            "name": "Movie 3",
            "actors": [
                {
                    "actor_id": "actor_2",
                    "role": "hero",
                    "is_debut_movie": False
                },
                {
                    "actor_id": "actor_4",
                    "role": "comedian",
                    "is_debut_movie": True
                },
                {
                    "actor_id": "actor_5",
                    "role": "side character",
                    "is_debut_movie": True
                }
            ],
            "box_office_collection_in_crores": "16.3",
            "release_date": "2010-5-3",
            "director_name": "Director 2"
        },
        {
            "movie_id": "movie_4",
            "name": "Movie 4",
            "actors": [
                {
                    "actor_id": "actor_2",
                    "role": "hero",
                    "is_debut_movie": False
                },
                {
                    "actor_id": "actor_3",
                    "role": "villan",
                    "is_debut_movie": True
                },
                {
                    "actor_id": "actor_1",
                    "role": "comedian",
                    "is_debut_movie": True
                },
                {
                    "actor_id": "actor_5",
                    "role": "side character",
                    "is_debut_movie": True
                }
            ],
            "box_office_collection_in_crores": "17.3",
            "release_date": "2008-5-3",
            "director_name": "Director 2"
        }
    ]
directors_list = [
        "Director 1","Director 2"
    ]
movie_rating_list = [
        {
            "movie_id": "movie_1",
            "rating_one_count": 4,
            "rating_two_count": 4,
            "rating_three_count": 4,
            "rating_four_count": 4,
            "rating_five_count": 4
        },
        {
            "movie_id": "movie_2",
            "rating_one_count": 6,
            "rating_two_count": 3,
            "rating_three_count": 7,
            "rating_four_count": 8,
            "rating_five_count": 5
        },
        {
            "movie_id": "movie_3",
            "rating_one_count": 4,
            "rating_two_count": 3,
            "rating_three_count": 9,
            "rating_four_count": 8,
            "rating_five_count": 3
        },
        {
            "movie_id": "movie_4",
            "rating_one_count": 2,
            "rating_two_count": 7,
            "rating_three_count": 4,
            "rating_four_count": 9,
            "rating_five_count": 5
        }
        
    ]


def populate_database(actors_list, movies_list, directors_list, movie_rating_list):
    
    actors_lst = []
    for actor in actors_list:
        if not(actor['gender']):
            actor['gender'] = None
        actors_lst.append(
            Actor(
                actor_id = actor['actor_id'],
                name = actor['name'],
                gender = actor['gender']
            )
        )
    Actor.objects.bulk_create(actors_lst)
        
    
    Director.objects.bulk_create(
        [ Director(name=director) for director in directors_list ]
    )
    
    movie_list = []    
    cast_list = []
    for movie in movies_list:
        movie_list.append(
            Movie(movie_id = movie['movie_id'],
            name = movie['name'],
            box_office_collection_in_crores = movie['box_office_collection_in_crores'],
            release_date = movie['release_date'],
            director = Director.objects.get(name = movie['director_name'])
            )
        )
        for actor in movie['actors']:
            cast_list.append(
                Cast(
                    actor_id = actor['actor_id'],
                    movie_id = movie['movie_id'],
                    role = actor['role'],
                    is_debut_movie = actor['is_debut_movie']
            ))
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

def remove_all_actors_from_given_movie(movie_object):
    
    movie_object.actors.clear()
    
def get_all_rating_objects_for_given_movies(movie_objs):
    
    return list(Rating.objects.filter(movie__in = movie_objs))

def get_movies_by_given_movie_objects(movie_objs):
    movies_list = []
    for movie_obj in movie_objs:
        casts_list = []
        for cast_obj in movie_obj.moviecast.all():
            cast_dict = {}
            actor_dict = {}
            actor_dict['name'] = cast_obj.actor.name
            actor_dict['actor_id'] = cast_obj.actor.actor_id
            cast_dict['actor'] = actor_dict
            cast_dict['role'] = cast_obj.role
            cast_dict['is_debut_movie'] = cast_obj.is_debut_movie
            casts_list.append(cast_dict)
        movie_dict = {}
        movie_dict['movie_id'] = movie_obj.movie_id
        movie_dict['name'] = movie_obj.name
        movie_dict['cast'] = casts_list
        movie_dict['box_office_collection_in_crores'] = movie_obj.box_office_collection_in_crores
        movie_dict['release_date'] = str(movie_obj.release_date)
        movie_dict['director_name'] = movie_obj.director.name
        movie_dict['average_rating'] = get_average_rating_of_movie(movie_obj)
        movie_dict['total_number_of_ratings'] = total_number_of_ratings(movie_obj)
        movies_list.append(movie_dict)
    return movies_list

def get_movies_by_given_movie_names(movie_names):
    movie_objs = Movie.objects.filter(
        name__in=movie_names).select_related('director','rating').prefetch_related('moviecast__actor')
    return get_movies_by_given_movie_objects(movie_objs)

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
        return (rate_obj.rating_one_count 
                + rate_obj.rating_two_count
                + rate_obj.rating_three_count
                + rate_obj.rating_four_count  
                + rate_obj.rating_five_count
            )
    except Rating.DoesNotExist:
        return 0
        
def get_all_actor_objects_acted_in_given_movies(movie_objs):
    return Actor.objects.filter(actorcast__movie__in=movie_objs).distinct()

def get_average_box_office_collections():
    
    try:
        return round(
        Movie.objects.aggregate(
        average_movie_collections = 
        Avg('box_office_collection_in_crores')
        )['average_movie_collections'],3)
    except:
        return 0

def reset_ratings_for_movies_in_given_year(year):
    Rating.objects.filter(
        movie__release_date__year=year
            ).update(
                rating_one_count=0,
                rating_two_count=0,
                rating_three_count=0,
                rating_four_count=0,
                rating_five_count=0)
"""
    female_count = Count('actors',distinct = True,filter = Q(actors__gender='FEMALE'))
    Movie.objects.annotate(
        female_count = female_count).filter(
            female_count__gte=5).select_related(
                'director','rating').prefetch_related(
                    'moviecast__actor')
"""

def get_movies_with_distinct_actors_count():
    
    return Movie.objects.annotate(
        actors_count = Count('actors',distinct = True)
        )

def get_male_and_female_actors_count_for_each_movie():
    
    male_count = Count('actors',distinct = True,filter = Q(actors__gender='MALE'))
    female_count = Count('actors',distinct = True,filter = Q(actors__gender='FEMALE'))
    return Movie.objects.annotate(
        male_actors_count = male_count,female_actors_count = female_count
        )

    
def get_no_of_movies_and_distinct_roles_for_each_actor():
    
    return list(Actor.objects.annotate(
        movies_count = Count('cast__movie',distinct = True),
        roles_count = Count('cast__role',distinct = True)
        ))

    

    
    
