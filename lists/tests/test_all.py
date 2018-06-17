from django.urls import resolve
from django.test import TestCase
from django.http import HttpRequest
from django.template.loader import render_to_string

from lists.views import home_page
from lists.models import Movie, List


class HomePageTest(TestCase):

    def test_uses_home_template(self):
        response = self.client.get('/')
        self.assertTemplateUsed(response, 'home.html')


class ListAndItemModelTest(TestCase):

    def test_saving_and_retrieving_movies(self):
        movielist = List()
        movielist.save()

        first_movie = Movie()
        first_movie.title = 'The first (ever) movie title'
        first_movie.movielist = movielist
        first_movie.save()

        second_movie = Movie()
        second_movie.title = 'The sequel to the first movie title'
        second_movie.movielist = movielist
        second_movie.save()

        saved_list = List.objects.first()
        self.assertEqual(saved_list, movielist)

        saved_movies = Movie.objects.all()
        self.assertEqual(saved_movies.count(), 2)

        first_saved_movie = saved_movies[0]
        second_saved_movie = saved_movies[1]
        self.assertEqual(first_saved_movie.title, 'The first (ever) movie title')
        self.assertEqual(first_saved_movie.movielist, movielist)
        self.assertEqual(second_saved_movie.title, 'The sequel to the first movie title')
        self.assertEqual(second_saved_movie.movielist, movielist)


class ListViewTest(TestCase):

    def test_uses_list_template(self):
        movielist = List.objects.create()
        response = self.client.get(f'/lists/{movielist.id}/')
        self.assertTemplateUsed(response, 'list.html')

    
    def test_displays_only_movies_for_that_list(self):
        correct_list = List.objects.create()
        Movie.objects.create(title='moviey 1', movielist=correct_list)
        Movie.objects.create(title='moviey 2', movielist=correct_list)
        other_list = List.objects.create()
        Movie.objects.create(title='other list movie 1', movielist=other_list)
        Movie.objects.create(title='other list movie 2', movielist=other_list)

        response = self.client.get(f'/lists/{correct_list.id}/')

        self.assertContains(response, 'moviey 1')
        self.assertContains(response, 'moviey 2')
        self.assertNotContains(response, 'other list movie 1')
        self.assertNotContains(response, 'other list movie 2')


    def test_passes_correct_list_to_template(self):
        other_list = List.objects.create()
        correct_list = List.objects.create()
        response = self.client.get(f'/lists/{correct_list.id}/')
        self.assertEqual(response.context['list'], correct_list)


class NewListTest(TestCase):

    def test_can_save_a_POST_request(self):
        self.client.post('/lists/new', data={'movie_title': 'A new movie title'})
        self.assertEqual(Movie.objects.count(), 1)
        new_movie = Movie.objects.first()
        self.assertEqual(new_movie.title, 'A new movie title')


    def test_redirects_after_POST(self):
        response = self.client.post('/lists/new', data={'movie_title': 'A new movie title'})
        new_list = List.objects.first()
        self.assertRedirects(response, f'/lists/{new_list.id}/')


    def test_can_save_a_POST_request_to_an_existing_list(self):
        other_list = List.objects.create()
        correct_list = List.objects.create()

        self.client.post(
            f'/lists/{correct_list.id}/add_movie',
            data={'movie_title': 'A new movie title for an existing list'}
        )

        self.assertEqual(Movie.objects.count(), 1)
        new_movie = Movie.objects.first()
        self.assertEqual(new_movie.title, 'A new movie title for an existing list')
        self.assertEqual(new_movie.movielist, correct_list)

    def test_redirects_to_list_view(self):
        other_list = List.objects.create()
        correct_list = List.objects.create()
        
        response = self.client.post(
            f'/lists/{correct_list.id}/add_movie',
            data={'movie_title': 'A new movie title for an existing list'}
        )
        
        self.assertRedirects(response, f'/lists/{correct_list.id}/')

