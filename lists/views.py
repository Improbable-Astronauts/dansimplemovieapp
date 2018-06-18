from django.shortcuts import redirect, render
from django.core.exceptions import ValidationError

from lists.models import Movie, List


def home_page(request):
    if request.method == 'POST':
        Movie.objects.create(title=request.POST['movie_title'])
        return redirect('/lists/the-only-list-in-the-world/')
    return render(request, 'home.html')


def view_list(request, list_id):
    movie_list = List.objects.get(id=list_id)
    error = None

    if request.method == 'POST':
        try:
            new_movie = Movie(title=request.POST['movie_title'], movielist=movie_list)
            new_movie.full_clean()
            new_movie.save()
            return redirect(movie_list)
        except ValidationError:
            error = "You can't have an empty movie title"

    return render(request, 'list.html', {'list': movie_list, 'error': error})


def new_list(request):
    movie_list = List.objects.create()
    new_movie = Movie.objects.create(title=request.POST['movie_title'], movielist=movie_list)
    try:
        new_movie.full_clean()
        new_movie.save()
    except ValidationError:
        movie_list.delete()
        error = "You can't have an empty movie title"
        return render(request, 'home.html', {"error": error})
    return redirect(movie_list)


