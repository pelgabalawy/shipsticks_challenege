"""Test: Step 1 booking flow — happy path."""
from pages.booking_page import BookingPage
from pages.home_page import HomePage


class TestBookingStep1:
    """
    Happy path: complete Step 1 with the required test data,
    assert Step 1 is done, and Step 2 is ready.
    """

    def test_step1_happy_path(self, page, test_data):

        # home page instance
        home = HomePage(page)

        # navigate to home
        home.go_to_home()

        #  fill get started form:
            # trip type
            # where from
            # where to
            # click save button
        home.select_origin_n_destination(test_data["shipment_type"],
                                            test_data["origin"],
                                            test_data["destination"])

        # wait for redirect to booking/ship
        expected_route = "/book/ship"
        page.wait_for_url(f"**{expected_route}**", timeout=5000)
        assert expected_route in page.url

        # start filling up step 1 form
        booking = BookingPage(page)

        # click I understand
        booking.accept_the_user_notification()

        # adding Golf Bag to the cart
        item_to_add, item_size = test_data["item"].split(" (")
        item_size = item_size[:-1]
        booking.add_item(item_to_add)

        # specify the size of the item to standard
        booking.select_item_size(item_size)

        # assert the correct size is selected (aria-checked="true")
        assert booking.is_size_selected(item_size), f"Size '{item_size}' is not selected"

        # assert the item was added — "Item Sizes" section only appears when an item is in the cart
        # the app uses plural labels (e.g. "Golf Bags") so we append "s" to match the DOM
        assert booking.is_item_added(item_to_add + "s", item_size), "Item was not added to the cart"

        # adding the delivery date
        booking.select_delivery_date(test_data["delivery_date"])

        # assert the dates on the service options are before the delivery date
        assert booking.validate_service_dates_before_delivery(test_data["delivery_date"])

        # select service level
        booking.select_service_level(test_data["service_level"])

        # click next traveler details
        booking.click_next_traveler_details()

        # verify you got redirected to book/login
        page.wait_for_url("**/book/login**", timeout=7000)
        assert "/book/login" in page.url

        # assert that shipping options is complete with a green check mark
        assert booking.is_shipping_options_complete(), "Booking step 1 did NOT complete!"
