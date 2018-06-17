from django.test import TestCase
from lists.models import Movie, List


class HomePageTest(TestCase):

    def test_uses_home_template(self):
        response = self.client.get('/')
        self.assertTemplateUsed(response, 'home.html')


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


class NewItemTest(TestCase):

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


class ListViewTest(TestCase):

    def test_uses_list_template(self):
        movielist = List.objects.create()
        response = self.client.get(f'/lists/{movielist.id}/')
        self.assertTemplateUsed(response, 'list.html')

    
    def test_passes_correct_list_to_template(self):
        other_list = List.objects.create()
        correct_list = List.objects.create()
        response = self.client.get(f'/lists/{correct_list.id}/')
        self.assertEqual(response.context['list'], correct_list)


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


