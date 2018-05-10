from django.urls import resolve
from django.test import TestCase
from django.http import HttpRequest
from django.template.loader import render_to_string

from lists.views import home_page
from lists.models import Movie


class HomePageTest(TestCase):

    def test_uses_home_template(self):
        response = self.client.get('/')
        self.assertTemplateUsed(response, 'home.html')

    def test_can_save_a_POST_request(self):
        response = self.client.post('/', data={'movie_title': 'A new movie title'})
        self.assertIn('A new movie title', response.content.decode())
        self.assertTemplateUsed(response, 'home.html')
        
class ItemModelTest(TestCase):
    
    def test_saving_and_retrieving_items(self):
        first_movie = Movie()
        first_movie.title = 'The first (ever) movie title'
        first_movie.save()

        second_movie = Movie()
        second_movie.title = 'The sequel to the first movie title'
        second_movie.save()

        saved_movies = Movie.objects.all()
        self.assertEqual(saved_movies.count(), 2)

        first_saved_movie = saved_movies[0]
        second_saved_movie = saved_movies[1]
        self.assertEqual(first_saved_movie.title, 'The first (ever) movie title')
        self.assertEqual(second_saved_movie.title, 'The sequel to the first movie title')

