from selenium.webdriver.common.keys import Keys
from unittest import skip
from .base import FunctionalTest


class ItemValidationTest(FunctionalTest):

    def test_cannot_add_empty_list_items(self):
        # Margo goes to the home page and accidentally tries to submit
        # an empty movie title. They hit Enter on the empty input box
        self.browser.get(self.live_server_url)
        self.browser.find_element_by_id('id_new_movie').send_keys(Keys.ENTER)

        # The home page refreshes, and there is an error message saying
        # that movie titles cannot be blank
        self.wait_for(lambda: self.assertEqual(
            self.browser.find_element_by_css_selector('.has-error').text,
            "You can't have an empty movie title"
        ))

        # They try again with some text for the movie title, which now works
        self.browser.find_element_by_id('id_new_movie').send_keys('Solo')
        self.browser.find_element_by_id('id_new_movie').send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: Solo')

        # Perversely, they now decide to submit a second blank movie title
        self.browser.find_element_by_id('id_new_movie').send_keys(Keys.ENTER)

        # They receive a similar warning on the movielist page
        self.wait_for(lambda: self.assertEqual(
            self.browser.find_element_by_css_selector('.has-error').text,
            "You can't have an empty movie title"
        ))

        # And they can correct it by filling some text in
        self.browser.find_element_by_id('id_new_movie').send_keys('Boxtrolls')
        self.browser.find_element_by_id('id_new_movie').send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: Solo')
        self.wait_for_row_in_list_table('2: Boxtrolls')



