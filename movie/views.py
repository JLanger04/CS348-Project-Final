from django.shortcuts import render, redirect, get_object_or_404
from django.db import connection, transaction
from .forms import CreateAndRateMovieForm, EditMovieForm
from .models import Ranked, Movies, Director, Main_Actor

def main_page(request):
    return render(request, 'main.html')
@transaction.atomic
def create_and_rate_movie(request):
    if request.method == 'POST':
        form = CreateAndRateMovieForm(request.POST)
        if form.is_valid():
            movie = form.save()
            rating = form.cleaned_data['rating']
            Ranked.objects.create(movie=movie, rating=rating)
            return redirect('create_and_rate_movie')
    else:
        form = CreateAndRateMovieForm()
    return render(request, 'create_movie.html', {'form': form})

@transaction.atomic
def edit_movie(request):
    movies = Movies.objects.all()
    if request.method == 'POST':
        form = EditMovieForm(request.POST, movies=movies)
        if form.is_valid():
            movie_id = form.cleaned_data['movie'].id
            title = form.cleaned_data['title']
            release_year = form.cleaned_data['release_year']
            duration = form.cleaned_data['duration']
            main_actor_id = form.cleaned_data['main_actor'].id
            director_id = form.cleaned_data['director'].id
            rating = form.cleaned_data['rating']
            
            Ranked.objects.update_or_create(
                movie_id=movie_id,
                defaults={'rating': rating}
            )
            
            movie = Movies.objects.get(pk=movie_id)
            movie.title = title
            movie.release_year = release_year
            movie.duration = duration
            movie.main_actor_id = main_actor_id
            movie.director_id = director_id
            movie.save()
            
            return redirect('edit_movie')
    else:
        form = EditMovieForm(movies=movies)
    
    return render(request, 'edit_movie.html', {'form': form})


@transaction.atomic
def delete_movie(request):
    if request.method == 'POST':
        movie_id = request.POST.get('movie_id')
        movie = get_object_or_404(Movies, pk=movie_id)
        Ranked.objects.filter(movie=movie).delete()
        movie.delete()
    movies = Movies.objects.all()
    return render(request, 'delete_movie.html', {'movies': movies})


def report_movie(request):
    directors = Director.objects.all()
    actors = Main_Actor.objects.all()

    selected_director = None
    selected_actor = None
    start_year = None
    end_year = None
    lower_rating = None
    higher_rating = None

    if request.method == 'POST':
        selected_director_id = request.POST.get('director')
        selected_actor_id = request.POST.get('actor')
        start_year = request.POST.get('start_year')
        end_year = request.POST.get('end_year')
        lower_rating = request.POST.get('lower_rating')
        higher_rating = request.POST.get('higher_rating')

        if selected_director_id:
            try:
                selected_director = Director.objects.get(pk=selected_director_id)
            except Director.DoesNotExist:
                pass
        if selected_actor_id:
            try:
                selected_actor = Main_Actor.objects.get(pk=selected_actor_id)
            except Main_Actor.DoesNotExist:
                pass

    query_averages = """
        SELECT AVG(m.duration), AVG(m.release_year), AVG(r.rating)
        FROM movie_movies m 
        LEFT JOIN movie_ranked r ON m.id = r.movie_id
        WHERE 1=1
    """

    query_movies = """
        SELECT m.title, m.release_year, m.duration, r.rating, d.name AS director_name, a.name AS main_actor_name
        FROM movie_movies m 
        LEFT JOIN movie_ranked r ON m.id = r.movie_id
        LEFT JOIN movie_director d ON m.director_id = d.id
        LEFT JOIN movie_main_actor a ON m.main_actor_id = a.id
        WHERE 1=1
    """

    conditions = []
    params = []

    if selected_director:
        conditions.append("m.director_id = %s")
        params.append(selected_director.id)
    if selected_actor:
        conditions.append("m.main_actor_id = %s")
        params.append(selected_actor.id)
    if start_year:
        conditions.append("m.release_year >= %s")
        params.append(start_year)
    if end_year:
        conditions.append("m.release_year <= %s")
        params.append(end_year)
    if lower_rating:
        conditions.append("r.rating >= %s")
        params.append(lower_rating)
    if higher_rating:
        conditions.append("r.rating <= %s")
        params.append(higher_rating)

    if conditions:
        query_averages += " AND " + " AND ".join(conditions)
        query_movies += " AND " + " AND ".join(conditions)


    with connection.cursor() as cursor:
            cursor.execute(query_averages, params)
            averages = cursor.fetchone()

            cursor.execute(query_movies, params)
            movies = cursor.fetchall()

    context = {
        'directors': directors,
        'actors': actors,
        'averages': averages,
        'movies': movies,
    }

    return render(request, 'report_interface.html', context)

