from django.shortcuts import redirect, render

from lists.models import Movie, List


def home_page(request):
    if request.method == 'POST':
        Movie.objects.create(title=request.POST['movie_title'])
        return redirect('/lists/the-only-list-in-the-world/')
    return render(request, 'home.html')


def view_list(request, list_id):
    movielist = List.objects.get(id=list_id)
    return render(request, 'list.html', {'list': movielist})


def new_list(request):
    movielist = List.objects.create()
    Movie.objects.create(title=request.POST['movie_title'], movielist=movielist)
    return redirect(f'/lists/{movielist.id}/')


def add_movie(request, list_id):
    movielist = List.objects.get(id=list_id)
    Movie.objects.create(title=request.POST['movie_title'], movielist=movielist)
    return redirect(f'/lists/{movielist.id}/')

