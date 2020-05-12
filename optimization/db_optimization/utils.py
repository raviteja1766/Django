from db_optimization.models import *
from django.db import *

def profile():
    def decorator(func):
        def handler(*args, **kwargs):
            import line_profiler
            profiler = line_profiler.LineProfiler()
            profiler.enable_by_count()
            profiler.add_function(func)
            result = func(*args, **kwargs)
            profiler.print_stats()
            return result

        handler.__doc__ = func.__doc__
        return handler

    return decorator


book_ids = [23,456,24,87,65,9,6,3,7,12]

@profile()
def get_books_by_library_id(book_ids):
    from collections import defaultdict
    result = defaultdict(list)
   
    for book_id in book_ids:
        book = Book.objects.get(id=book_id)
        result[book.library_id].append(book)
    return result

@profile()
def get_books_by_library_id_one_query(book_ids):
    from collections import defaultdict
    books = Book.objects.filter(id__in=book_ids)
    result = defaultdict(list)
    
    for book in books:
        result[book.library_id].append(book)
    return result

@profile()
def get_books_by_author():
    from collections import defaultdict    
    books = Book.objects.all()
    result = defaultdict(list)
    for book in books[:100]:
        author = book.author
        title_and_author = '{} by {}'.format(
            book.title,
            author.name
        )
        result[book.library_id].append(title_and_author)
    return result

    
@profile()    
def get_books_by_author_select_related():
    from collections import defaultdict
    books = Book.objects.all().select_related('author')
    result = defaultdict(list)
    for book in books[:10]:
        author = book.author
        title_and_author = '{} by {}'.format(
            book.title,
            author.name
        )
        result[book.library_id].append(title_and_author)
    return result

@profile()
def get_books_by_author_select_related_values():
    from collections import defaultdict
    books = (
        Book.objects
         .all()
         .values('title', 'library_id', 'author__name')[:10]
    )
    result = defaultdict(list)
    for book in books.iterator():
        title_and_author = '{} by {}'.format(
            book['title'],
            book['author__name']
        )
        result[book['library_id']].append(title_and_author)
    
    return result
    
@profile()    
def get_books_by_author_select_related_values_list():
    from collections import defaultdict
    books = (
        Book.objects
         .all()
         .values_list('title', 'library_id', 'author__name')[:10]
    )
    result = defaultdict(list)
    for book in books.iterator():
        title_and_author = '{} by {}'.format(
            book[0],
            book[2]
        )
        result[book[1]].append(title_and_author)
    
    return result

@profile()
def get_page_count_by_library_id():
    from collections import defaultdict
    result = defaultdict(int)
    books = Book.objects.all().prefetch_related('pages')[:10]
    for book in books:
        result[book.library_id] += book.get_page_count()
    return result

@profile()
def get_page_count_by_library_id_using_annotation():                                                    
    from django.db.models import Sum
    result = {}
    libraries = (
        Library.objects
        .all()
        .annotate(page_count=Sum('books__pages'))
        .values_list('id', 'page_count')[:10]
    )
    for library_id, page_count in libraries:
        result[library_id] = page_count
    return result

toppings_list = [
        'topping1','topping2','topping3','topping4','topping5','topping6',
        'topping7','topping8','topping9','topping10','topping11','topping12'
    ]

pizzas_list = [
        {
            'name':'pizza1',
            'toppings':[
                    'topping2','topping6','topping4','topping8'
                ]
        },
        {
            'name':'pizza2',
            'toppings':[
                    'topping1','topping5','topping2','topping7'
                ]
        },
        {
            'name':'pizza3',
            'toppings':[
                    'topping2','topping6','topping4','topping8'
                ]
        },
        {
            'name':'pizza4',
            'toppings':[
                    'topping2','topping6','topping4','topping8'
                ]
        },
        {
            'name':'pizza5',
            'toppings':[
                    'topping2','topping6','topping4','topping8'
                ]
        },
        {
            'name':'pizza6',
            'toppings':[
                    'topping2','topping6','topping4','topping8'
                ]
        },
        {
            'name':'pizza7',
            'toppings':[
                    'topping2','topping6','topping4','topping8'
                ]
        },
        {
            'name':'pizza8',
            'toppings':[
                    'topping2','topping6','topping4','topping8'
                ]
        },
        {
            'name':'pizza9',
            'toppings':[
                    'topping2','topping6','topping4','topping8'
                ]
        },
        {
            'name':'pizza10',
            'toppings':[
                    'topping2','topping6','topping4','topping8'
                ]
        },
        {
            'name':'pizza11',
            'toppings':[
                    'topping2','topping6','topping4','topping8'
                ]
        }
    ]
restaurants_list = [
        {
            'best_pizza':'pizza3',
            'pizzas':['pizza2','pizza7','pizza6','pizza8','pizza10']
        },
        {
            'best_pizza':'pizza4',
            'pizzas':['pizza2','pizza7','pizza6','pizza8','pizza10']
        },
        {
            'best_pizza':'pizza3',
            'pizzas':['pizza2','pizza7','pizza6','pizza8','pizza10']
        },
        {
            'best_pizza':'pizza1',
            'pizzas':['pizza2','pizza7','pizza6','pizza8','pizza10']
        },
        {
            'best_pizza':'pizza2',
            'pizzas':['pizza2','pizza7','pizza6','pizza8','pizza10']
        },
        {
            'best_pizza':'pizza5',
            'pizzas':['pizza2','pizza7','pizza6','pizza8','pizza10']
        }
    
    ]
def populate_toppings():
    
    toppings = [Topping(name = topping) for topping in toppings_list]
    Topping.objects.bulk_create(toppings)
    
def populate_pizzas():
     
    for pizza in pizzas_list:
        pz = Pizza.objects.create(
                name = pizza['name']
                )
        topping_list = []
        for topping in pizza['toppings']:
            topping_list.append(Topping.objects.get(name=topping))
        pz.toppings.set(topping_list)
        
def populate_restaurant():
    
    for restaurant in restaurants_list:
        rs = Restaurant.objects.create(best_pizza = Pizza.objects.get(name=restaurant['best_pizza']))
        pizza_list = []
        for pizza in restaurant['pizzas']:
            pizza_list.append(Pizza.objects.get(name = pizza))
        rs.pizzas.set(pizza_list)
    
    
    
    
        