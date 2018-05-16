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
        self.client.post('/', data={'movie_title': 'A new movie title'})

        self.assertEqual(Movie.objects.count(), 1)
        new_movie = Movie.objects.first()
        self.assertEqual(new_movie.title, 'A new movie title')


    def test_redirects_after_POST(self):
        response = self.client.post('/', data={'movie_title': 'A new movie title'})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response['location'], '/lists/the-only-list-in-the-world')


    def test_only_saves_movies_when_necessary(self):
        self.client.get('/')
        self.assertEqual(Movie.objects.count(), 0)


class ItemModelTest(TestCase):

    def test_saving_and_retrieving_movies(self):
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


class ListViewTest(TestCase):

    def test_uses_list_template(self):
        response = self.client.get('/lists/the-only-list-in-the-world/')
        self.assertTemplateUsed(response, 'list.html')

    
    def test_displays_all_movies(self):
        Movie.objects.create(title='moviey 1')
        Movie.objects.create(title='moviey 2')

        response = self.client.get('/lists/the-only-list-in-the-world/')

        self.assertContains(response, 'moviey 1')
        self.assertContains(response, 'moviey 2')


