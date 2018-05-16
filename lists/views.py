from django.shortcuts import redirect, render
from lists.models import Movie

def home_page(request):
    if request.method == 'POST':
        Movie.objects.create(title=request.POST['movie_title'])
        return redirect('/lists/the-only-list-in-the-world')
    return render(request, 'home.html')

def view_list(request):
    movies = Movie.objects.all()
    return render(request, 'list.html', {'movies': movies})

