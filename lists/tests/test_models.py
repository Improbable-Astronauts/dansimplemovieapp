from django.test import TestCase
from django.core.exceptions import ValidationError
from lists.models import Movie, List


class ListAndMovieModelsTest(TestCase):

    def test_saving_and_retrieving_movies(self):
        movie_list = List()
        movie_list.save()

        first_movie = Movie()
        first_movie.title = 'The first (ever) movie title'
        first_movie.movielist = movie_list
        first_movie.save()

        second_movie = Movie()
        second_movie.title = 'The sequel to the first movie title'
        second_movie.movielist = movie_list
        second_movie.save()

        saved_list = List.objects.first()
        self.assertEqual(saved_list, movie_list)

        saved_movies = Movie.objects.all()
        self.assertEqual(saved_movies.count(), 2)

        first_saved_movie = saved_movies[0]
        second_saved_movie = saved_movies[1]
        self.assertEqual(first_saved_movie.title, 'The first (ever) movie title')
        self.assertEqual(first_saved_movie.movielist, movie_list)
        self.assertEqual(second_saved_movie.title, 'The sequel to the first movie title')
        self.assertEqual(second_saved_movie.movielist, movie_list)


    def test_cannot_save_empty_movie_lists(self):
        movie_list = List.objects.create()
        empty_movie = Movie(movielist=movie_list, title='')
        with self.assertRaises(ValidationError):
            empty_movie.save()
            empty_movie.full_clean()  # Run full validation, don't assume that the db will silently ignore 


