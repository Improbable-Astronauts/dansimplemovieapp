from selenium import webdriver
import unittest

class NewVisitorTest(unittest.TestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()


    def tearDown(self):
        self.browser.quit()

    def test_can_start_a_list_and_retrieve_it_later(self):
        # Margo likes movies and keeps a list of the movies they have watched.
        # They heard about a new online app that allows the user to keep a list of
        # movies. Margo visits the movielists homepage
        self.browser.get('http://localhost:8000')
        
        # They notice that they page title and header mention movie lists
        self.assertIn('Movie Lists', self.browser.title)
        self.fail('Finish the test!')
        
        # They are invited to enter a movie title straight away
        
        # They type "The Terminator" into a text box (Margo remembers when movies
        # were original)
        
        # When they hit enter, the page updates, and now the page lists
        # "1: The Terminator" as a movie title in a movie list
        
        # There is still a text box inviting them to add another item. They
        # enter "Finding Nemo" (Margo has a nephew visit from time to time)
        
        # The page updates again, and now shows both movie titles on their list
        
        # Margo wonders whether the site will remember their list. Then they see that
        # the site has generated a unique URL for them -- there is some explanatory
        # text to that effect.
        
        # They visit that URL - their movie list is still there.
        
        # Satisfied, Margo goes back to sleep.

if __name__ == '__main__':
    unittest.main(warnings='ignore')
