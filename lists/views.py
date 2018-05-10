from django.shortcuts import render

def home_page(request):
    return render(request, 'home.html', {
        'new_movie_title': request.POST.get('movie_title', ''),
    })

