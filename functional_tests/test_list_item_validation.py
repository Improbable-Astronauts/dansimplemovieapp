from selenium.webdriver.common.keys import Keys
from unittest import skip
from .base import FunctionalTest


class ItemValidationTest(FunctionalTest):

    def test_cannot_add_empty_list_items(self):
        # Margo goes to the home page and accidentally tries to submit
        # an empty movie title. They hit Enter on the empty input box

        # The home page refreshes, and there is an error message saying
        # that movie titles cannot be blank

        # They try again with some text for the movie title, which now works

        # Perversely, they now decide to submit a second blank movie title

        # They receive a similar warning on the movielist page

        # And they can correct it by filling some text in
        self.fail('write me!')



