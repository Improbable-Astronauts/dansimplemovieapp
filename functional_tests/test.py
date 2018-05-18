from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import WebDriverException
import time

MAX_WAIT = 10


class NewVisitorTest(LiveServerTestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()


    def tearDown(self):
        self.browser.refresh()
        self.browser.quit()


    def wait_for_row_in_list_table(self, row_text):
        start_time = time.time()
        while True:
            try:
                table = self.browser.find_element_by_id('id_movie_table')
                rows = table.find_elements_by_tag_name('tr')
                self.assertIn(row_text, [row.text for row in rows])
                return
            except (AssertionError, WebDriverException) as e:
                if time.time() - start_time > MAX_WAIT:
                    raise e
                time.sleep(0.5)


    def test_can_start_a_list_for_one_user(self):
        # Margo likes movies and keeps a list of the movies they have watched.
        # They heard about a new online app that allows the user to keep a list of
        # movies. Margo visits the movielists homepage
        self.browser.get(self.live_server_url)
        
        # They notice that they page title and header mention movie lists
        self.assertIn('Movie Lists', self.browser.title)
        header_text = self.browser.find_element_by_tag_name('h1').text
        self.assertIn('Start a new Movie list', header_text)
        
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
        self.wait_for_row_in_list_table('1: The Terminator')

        # There is still a text box inviting them to add another item. They
        # enter "Finding Nemo" (Margo has a nephew visit from time to time)
        inputbox = self.browser.find_element_by_id('id_new_movie')
        inputbox.send_keys('Finding Nemo')
        inputbox.send_keys(Keys.ENTER)
        
        # The page updates again, and now shows both movie titles on their list
        self.wait_for_row_in_list_table('2: Finding Nemo')
        self.wait_for_row_in_list_table('1: The Terminator')
        
        # Satisfied, Margo goes back to sleep.

    def test_multiple_users_can_start_lists_at_different_urls(self):
        # Margo starts a new movie list
        self.browser.get(self.live_server_url)
        inputbox = self.browser.find_element_by_id('id_new_movie')
        inputbox.send_keys('The Terminator')
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: The Terminator')

        # They notice that their list has a unique URL
        margo_list_url = self.browser.current_url
        self.assertRegex(margo_list_url, '/lists/.+')

        # Now a new user, Carlos, comes along to the site.
        
        ## We use a new browser session to make sure that no information
        ## of Margo's is coming through from cookies, etc.
        self.browser.quit()
        self.browser = webdriver.Firefox()

        # Carlos visits the home page. There is no sign of Margo's list
        self.browser.get(self.live_server_url)
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('The Terminator', page_text)
        self.assertNotIn('Finding Nemo', page_text)

        # Carlos starts a new list by entering a new movie title.
        # They are less interesting than Margo
        inputbox = self.browser.find_element_by_id('id_new_movie')
        inputbox.send_keys("You've Got Mail")
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table("1: You've Got Mail")

        # Carlos gets their own unique URL
        carlos_list_url = self.browser.current_url
        self.assertRegex(carlos_list_url, '/lists/.+')
        self.assertNotEqual(carlos_list_url, margo_list_url)

        # Again, there is no trace of Margo's List
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('The Terminator', page_text)
        self.assertIn("You've Got Mail", page_text)
        
        # Satisfied, they both go back to sleep.
