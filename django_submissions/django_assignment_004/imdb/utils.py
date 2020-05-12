from imdb.models import *
from django.db.models import *
from django.db import *

"""
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
"""


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

def get_average_box_office_collections():
    
    try:
        return round(
        Movie.objects.aggregate(
        average_movie_collections = 
        Avg('box_office_collection_in_crores')
        )['average_movie_collections'],3)
    except:
        return 0


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

def get_roles_count_for_each_movie():
    
    return Movie.objects.annotate(
        roles_count = Count('cast__role',distinct = True)
        )

def get_role_frequency():
    role_count_list = Cast.objects.values('role').annotate(
            role_count = Count('actor',distinct = True)
            )
    role_dict = {}
    for role in role_count_list:
        role_dict[role['role']] = role['role_count']
    return role_dict

def get_role_frequency_in_order():
    return list(Cast.objects.values_list('role').annotate(
        Count('actor')    
        ).order_by('-movie__release_date'))
    
def get_no_of_movies_and_distinct_roles_for_each_actor():
    
    return list(Actor.objects.annotate(
        movies_count = Count('cast__movie',distinct = True),
        roles_count = Count('cast__role',distinct = True)
        ))
        
def get_movies_with_atleast_forty_actors():
    
    return Movie.objects.annotate(
        actors_count = Count('cast__actor',distinct = True)).filter(
            actors_count__gte = 40
            )

def get_average_no_of_actors_for_all_movies():
    
    try:
        return round(
        Movie.objects.annotate(
        actors_count = 
        Count('cast__actor',distinct = True)
        ).aggregate(
           average_actors = Avg('actors_count')
            )['average_actors'],3)
    except:
        return 0
    
    
    
