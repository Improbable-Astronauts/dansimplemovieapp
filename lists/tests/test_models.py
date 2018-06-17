from django.test import TestCase
from lists.models import Movie, List


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


