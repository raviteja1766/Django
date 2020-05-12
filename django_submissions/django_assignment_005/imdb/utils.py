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
        },
        {
            "actor_id": "actor_6",
            "name": "naveen kumar",
            "gender": "FEMALE"
        },
        {
            "actor_id": "actor_7",
            "name": "naveen kumar",
            "gender": "FEMALE"
        },
        {
            "actor_id": "actor_8",
            "name": "naveen kumar",
            "gender": "FEMALE"
        },
        {
            "actor_id": "actor_9",
            "name": "naveen kumar",
            "gender": "FEMALE"
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
                },
                {
                    "actor_id": "actor_6",
                    "role": "side character",
                    "is_debut_movie": True
                },
                {
                    "actor_id": "actor_7",
                    "role": "side character",
                    "is_debut_movie": True
                },
                {
                    "actor_id": "actor_8",
                    "role": "side character",
                    "is_debut_movie": True
                },
                {
                    "actor_id": "actor_9",
                    "role": "side character",
                    "is_debut_movie": True
                }
            ],
            "box_office_collection_in_crores": "12.3",
            "release_date": "1999-5-3",
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
            "release_date": "2005-5-3",
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
                    "actor_id": "actor_2",
                    "role": "villan",
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
            "release_date": "2010-5-3",
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



#task-1
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

#task-2
def remove_all_actors_from_given_movie(movie_object):
    
    movie_object.actors.clear()

#task-3    
def get_all_rating_objects_for_given_movies(movie_objs):
    
    return list(Rating.objects.filter(movie__in = movie_objs))

def get_average_rating_and_total_ratings_of_movie(movie_obj):
    
    try:
        rate_obj = movie_obj.rating
        one = rate_obj.rating_one_count 
        two = rate_obj.rating_two_count 
        three = rate_obj.rating_three_count 
        four = rate_obj.rating_four_count  
        five = rate_obj.rating_five_count 
        sum_of_ratings = one + two * 2 + three * 3 + four * 4 + five * 5
        no_of_ratings = one + two + three + four + five
        return [(sum_of_ratings/no_of_ratings),no_of_ratings]
    except ZeroDivisionError:
        return [0,0]
    except Rating.DoesNotExist:
        return [0,0]

#MovieDetails...
def get_movies_by_given_cast_objects(cast_objs):
    movie_lst = []
    movie_list=[]
    for cast in cast_objs:
        if cast.movie not in movie_lst:
            cast_list = []
            movie_lst.append(cast.movie)
            movie_obj = cast.movie
            average_ratings,total_ratings = get_average_rating_and_total_ratings_of_movie(movie_obj)
            movie_list.append({
                'movie_id': movie_obj.movie_id,
                'name': movie_obj.name,
                'cast': cast_list,
                'box_office_collection_in_crores': movie_obj.box_office_collection_in_crores,
                'release_date': str(movie_obj.release_date),
                'director_name': movie_obj.director.name,
                'average_rating': average_ratings,
                'total_number_of_ratings': total_ratings
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

#task-4
def get_movies_by_given_movie_names(movie_names):
    
    cast_objs = Cast.objects.filter(
                    movie__name__in=movie_names).select_related(
                        'movie__director','movie__rating','actor'
                    )
    return get_movies_by_given_cast_objects(cast_objs)
 
#task-5
def get_all_actor_objects_acted_in_given_movies(movie_objs):
    return list(Actor.objects.filter(movie__in=movie_objs).distinct())

#task-6
def get_female_cast_details_from_movies_having_more_than_five_female_cast():
    female_count = Count('actors',distinct = True,filter = Q(actors__gender='FEMALE'))
    cast_objs = Cast.objects.filter(movie__in=Movie.objects.annotate(
                    female_count = female_count).filter(female_count__gt=5)
                        ).filter(actor__gender='FEMALE').select_related(
                            'movie__director','movie__rating','actor'
                            )
    return get_movies_by_given_cast_objects(cast_objs)


#task-7
#get_actor_movies_released_in_year_greater_than_or_equal_to_2000
def get_actor_movies_released_in_year_greater_than_or_equal_to_2000():
    cast_objs = Cast.objects.filter(
        movie__in = Movie.objects.filter(release_date__year__gte=2000)).select_related(
                'movie__director','movie__rating','actor').order_by('actor','movie')
    actor_lst = []
    actors_list = []
    for cast in cast_objs:
        if cast.actor not in actor_lst:
            actor_lst.append(cast.actor)
            movies_list = []
            actor_obj = cast.actor
            actors_list.append({
                "name": actor_obj.name,
                "actor_id": actor_obj.actor_id,
                "movies": movies_list
            })
            movie_lst = []
        if  cast.movie not in movie_lst:
            movie_lst.append(cast.movie)
            movie_obj = cast.movie
            average_ratings,total_ratings = get_average_rating_and_total_ratings_of_movie(movie_obj)
            cast_list = []
            movies_list.append({
                "movie_id": movie_obj.movie_id,
                "name": movie_obj.name,
                "cast": cast_list,
                "box_office_collection_in_crores": movie_obj.box_office_collection_in_crores,
                "release_date": str(movie_obj.release_date),
                "director_name": movie_obj.director.name,
                "average_rating": average_ratings,
                "total_number_of_ratings": total_ratings
            })    
        cast_list.append({
        'role': cast.role,
        'is_debut_movie': cast.is_debut_movie
        })
    return actors_list

#task-8
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
#task-7
#get_actor_movies_released_in_year_greater_than_or_equal_to_2000
def real_get_actor_movies_released_in_year_greater_than_or_equal_to_2000():
    
    queryset = Movie.objects.filter(release_date__year__gte=2000).select_related('director','rating').prefetch_related(
            Prefetch('cast_set',to_attr = 'casts'))
    actor_objs = Actor.objects.filter(movie__release_date__year__gte=2000).prefetch_related(
            Prefetch('movie_set',queryset = queryset,to_attr = 'movies')
            )
    actors_list = []
    for actor in actor_objs:
        movies_list = []
        for movie in actor.movies:
            casts_list = []
            for cast in movie.casts:
                if cast.actor_id == actor.actor_id:
                    casts_list.append({
                        'role': cast.role,
                        'is_debut_movie': cast.is_debut_movie
                    })
            average_ratings,total_ratings = get_average_rating_and_total_ratings_of_movie(movie)
            movies_list.append({
                'movie_id': movie.movie_id,
                'name': movie.name,
                'cast': casts_list,
                'box_office_collection_in_crores': movie.box_office_collection_in_crores,
                'release_date': str(movie.release_date),
                'director_name': movie.director.name,
                "average_rating": average_ratings,
                "total_number_of_ratings": total_ratings
            })
        
        actors_list.append({
            'name': actor.name,
            'actor_id': actor.actor_id,
            'movies': movies_list
        })
    return actors_list
"""


    
    
    
    