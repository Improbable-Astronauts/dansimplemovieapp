from django.shortcuts import redirect, render
from lists.models import Movie

def home_page(request):
    if request.method == 'POST':
        Movie.objects.create(title=request.POST['movie_title'])
        return redirect('/')

    movies = Movie.objects.all()
    return render(request, 'home.html', {'movies': movies})

