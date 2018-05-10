from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
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
        header_text = self.browser.find_element_by_tag_name('h1').text
        self.assertIn('Movie List', header_text)
        
        # They are invited to enter a movie title straight away
        inputbox = self.browser.find_element_by_id('id_new_movie')
        self.assertEqual(
            inputbox.get_attribute('placeholder'),
            'Enter a movie title'
        )
        
        # They type "The Terminator" into a text box (Margo remembers when movies
        # were original)
        inputbox.send_keys('The Terminator')
        
        # When they hit enter, the page updates, and now the page lists
        # "1: The Terminator" as a movie title in a movie list
        inputbox.send_keys(Keys.ENTER)
        time.sleep(1)

        table = self.browser.find_element_by_id('id_movie_table')
        rows = table.find_elements_by_tag_name('tr')
        self.assertIn('1: The Terminator', [row.text for row in rows])

        # There is still a text box inviting them to add another item. They
        # enter "Finding Nemo" (Margo has a nephew visit from time to time)
        inputbox = self.browser.find_element_by_id('id_new_movie')
        inputbox.send_keys('Finding Nemo')
        inputbox.send_keys(Keys.ENTER)
        time.sleep(1)
        
        # The page updates again, and now shows both movie titles on their list
        table = self.browser.find_element_by_id('id_movie_table')
        rows = table.find_elements_by_tag_name('tr')
        self.assertIn('1: The Terminator', [row.text for row in rows])
        self.assertIn('2: Finding Nemo', [row.text for row in rows])
        
        # Margo wonders whether the site will remember their list. Then they see that
        # the site has generated a unique URL for them -- there is some explanatory
        # text to that effect.
        self.fail('Finish the test!')
        
        # They visit that URL - their movie list is still there.
        
        # Satisfied, Margo goes back to sleep.

if __name__ == '__main__':
    unittest.main(warnings='ignore')
