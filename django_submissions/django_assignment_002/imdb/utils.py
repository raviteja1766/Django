from imdb.models import *

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


def get_no_of_distinct_movies_actor_acted(actor_id):
    #return len(actor_id.movie_set.all().distinct())
    #return len(Actor.objects.get(actor_id = actor_id).movie_set.distinct())
    return len(Movie.objects.filter(actors__actor_id = actor_id).distinct())
    
def get_movies_directed_by_director(director_obj):
    
    return director_obj.movie_set.all()
    #return Movie.objects.filter(director = director_obj)
    
def get_average_rating_of_movie(movie_obj):
    
    try:
        rate_obj = Rating.objects.get(movie = movie_obj)
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

def delete_movie_rating(movie_obj):
    
    try:
        rating_obj = Rating.objects.get(movie = movie_obj)
    except Rating.DoesNotExist:
        return 0
    rating_obj.delete()

def get_all_actor_objects_acted_in_given_movies(movie_objs):
    
    return Actor.objects.filter(movie__in=movie_objs).distinct()
    
def update_director_for_given_movie(movie_obj, director_obj):
    
    movie_obj.director = director_obj
    movie_obj.save()

def get_distinct_movies_acted_by_actor_whose_name_contains_john():
    
    return Movie.objects.filter(actors__name__contains='john').distinct()
    
def remove_all_actors_from_given_movie(movie_obj):
    
    movie_obj.actors.clear()
    
def get_all_rating_objects_for_given_movies(movie_objs):
    
    return Rating.objects.filter(movie__in=movie_objs)

def get_all_distinct_actors_for_given_movie(movie_obj):
    
    return Actor.objects.filter(movie = movie_obj).distinct()