"""Page Object for Step 1 of the booking flow."""
from pages.base_page import BasePage
from datetime import datetime


class BookingPage(BasePage):

    # ==================== ELEMENTS ====================

    # --- Post-redirect notification ---

    @property
    def i_understand_button(self):
        """Popup confirmation button shown after redirect to /booking/ship."""
        # as I mentnioned on the home page this is my prefered way when available
        return self.page.get_by_role("button", name="I understand")

    # --- Item configuration ---

    def item_size_option(self, size_name, index=0):
        # I wanted to be smart about this element because it did gave me some unstability but it was resolved
        """Size selector button for an item (e.g. Standard, Staff/XL)."""
        size_map = {
            "Standard": "Max 42 lb. Standard",
            "Staff/XL": "Max 56 lb. Staff/XL",
        }
        full_name = size_map.get(size_name, size_name)
        return self.page.get_by_role("button", name=full_name, exact=True).nth(index)

    def golf_bags_input(self, index=0):
        """Numeric input showing the current golf bag count for item at index."""
        # there wasn't much unique to this element to be captured easily
        # so I had to use name starts with productLineCounters
        return self.page.locator("input[name^='productLineCounters.']").nth(index)

    # --- Date picker (react-day-picker / rdp) ---

    @property
    def date_picker_button(self):
        """Button that opens the delivery date calendar popup."""
        # The button used to open the date picker
        # same way with by_role + name
        return self.page.get_by_role("button", name="Please select a date")

    @property
    def calendar_next_arrow(self):
        """Right arrow button to navigate to the next month in the calendar."""
        # this was not so clear to capture since its within the date picker object with no unique attributes
        return self.page.locator(".rdp-month button span.icon-arrow-right").locator("..")

    @property
    def calendar_month_header(self):
        """Span showing the current month/year in the calendar (e.g. 'March 2026')."""
        # this was not so clear to capture since its within the date picker object with no unique attributes
        return self.page.locator(".rdp-month span.type-body-5")

    def calendar_day(self, aria_label):
        # this was not so clear to capture since its within the date picker object with no unique attributes
        """A specific day cell in the calendar, matched by aria-label (e.g. 'April 8, 2026')."""
        return self.page.locator(f".rdp-month div[aria-label='{aria_label}']")

    # --- Service level cards ---

    @property
    def service_level_cards(self):
        """All shipping service radio cards (excludes item size radios)."""
        return self.page.locator("[role='radiogroup'] [role='radio']").filter(has=self.page.locator("div.bg-slate-700"))

    def service_level_option(self, service_name):
        """Radio card for a shipping service (e.g. Ground, Next Day Express)."""
        return self.service_level_cards.filter(has_text=service_name)

    # --- Step completion ---

    @property
    def next_traveler_details_button(self):
        """Submit button to complete Step 1 and proceed to Step 2."""
        return self.page.get_by_role("button", name="Next: Traveler Details").first

    @property
    def step1_check_circle(self):
        """The check-circle icon in the step progress bar that replaces the step-1 number
        once Step 1 is completed. Located inside a md-max:hidden container, so we check
        for DOM attachment rather than visibility."""
        return self.page.locator("span.icon-check-circle-filled").first

    # ==================== ACTIONS ====================

    def go_to_booking(self):
        """Navigate to the booking landing page."""
        self.navigate("/book/ship")

    def accept_the_user_notification(self):
        """Dismiss the 'I understand' popup after redirect."""
        self.i_understand_button.click()

    def golf_bags_increase_button(self, index=0):
        """Plus button to increase golf bag count for item at index."""
        return self.page.get_by_label("Increase Golf Bags count").nth(index)

    def golf_bags_decrease_button(self, index=0):
        """Minus button to decrease golf bag count for item at index."""
        return self.page.get_by_label("Decrease Golf Bags count").nth(index)

    def add_golf_bags(self, count=1):
        """Adjust the golf bag count to the desired number using +/- buttons."""
        current = int(self.golf_bags_input(0).input_value())
        while current < count:
            self.golf_bags_increase_button(0).click()
            current += 1
        while current > count:
            self.golf_bags_decrease_button(0).click()
            current -= 1

    def add_luggage(self, count=1):
        # TODO: implement luggage item support
        pass

    def add_item(self, item_to_add):
        """Add an item to the cart by type name.
        Config uses singular 'Golf Bag' to match the challenge spec,
        but the app labels use plural 'Golf Bags'."""
        if item_to_add == "Golf Bag":
            self.add_golf_bags()
        elif item_to_add == "Luggage":
            self.add_luggage()

    def select_item_size(self, size_name, index=0):
        """Click the size option for an item (e.g. Standard or Staff/XL)."""
        self.item_size_option(size_name, index).click(timeout=10000)

    def select_shipping_date(self, date_str):
        pass

    def select_delivery_date(self, date_str):
        """Open the calendar, navigate to the correct month, and click the target day.

        Args:
            date_str: Full date string from config, e.g. "Wednesday, April 8, 2026".
        """

        dt = datetime.strptime(date_str, "%A, %B %d, %Y")
        target_month_year = dt.strftime("%B %Y")           # "April 2026"
        day_aria_label = dt.strftime("%B %#d, %Y")         # "April 8, 2026" (Windows strftime)

        # Open the date picker
        self.date_picker_button.scroll_into_view_if_needed()
        self.date_picker_button.click()
        self.page.wait_for_timeout(500)

        # Navigate forward until we reach the target month
        for _ in range(12):
            header_text = self.calendar_month_header.inner_text(timeout=3000)
            if target_month_year in header_text:
                break
            self.calendar_next_arrow.click()
            self.page.wait_for_timeout(300)

        # Click the target day
        self.calendar_day(day_aria_label).click()

    def select_service_level(self, service_name):
        """Select a shipping service card (e.g. Ground, Next Day Express)."""
        option = self.service_level_option(service_name)
        option.scroll_into_view_if_needed()
        option.click()

    def validate_service_dates_before_delivery(self, delivery_date_str):
        """Verify all service card 'Ships on' dates are before the delivery date.

        Args:
            delivery_date_str: e.g. "Wednesday, April 8, 2026" from config.

        Returns:
            True if all ship dates are before the delivery date, False otherwise.
        """
        delivery_date = datetime.strptime(delivery_date_str, "%A, %B %d, %Y").date()

        cards = self.service_level_cards
        count = cards.count()

        for i in range(count):
            card = cards.nth(i)
            # Ship date is in: div.bg-slate-700 > div.font-semibold (e.g. "03/23/2026")
            ship_date_text = card.locator("div.bg-slate-700 div.font-semibold").inner_text(timeout=15000)
            ship_date = datetime.strptime(ship_date_text.strip(), "%m/%d/%Y").date()
            if ship_date >= delivery_date:
                return False

        return True

    def is_item_added(self, item_name, size_name=None, index=0):
        """Checks that the 'Item Sizes' section is visible — this section only renders
        after an item has been added to the cart, making it a reliable indicator."""
        item_sizes_header = self.page.locator("strong").filter(has_text="Item Sizes").first
        try:
            item_sizes_header.wait_for(state="visible", timeout=5000)
            return True
        except:
            return False

    def is_size_selected(self, size_name):
        """Checks that the given size radio is checked (aria-checked='true').
        Uses .first to avoid strict mode violations from duplicate desktop/mobile layouts."""
        selected = self.page.locator(
            "[role='radiogroup'] [role='radio'][aria-checked='true']"
        ).filter(has_text=size_name).first
        return selected.is_visible()

    def click_next_traveler_details(self):
        """Click the submit button to complete Step 1 and move to Step 2."""
        self.next_traveler_details_button.scroll_into_view_if_needed()
        self.next_traveler_details_button.click()

    def is_shipping_options_complete(self):
        """Verify Step 1 is complete by checking the check-circle icon exists in the
        step progress bar. The icon is inside a CSS-hidden container (md-max:hidden),
        so we check DOM attachment instead of visibility."""
        try:
            self.step1_check_circle.wait_for(state="attached", timeout=5000)
            return True
        except:
            return False
