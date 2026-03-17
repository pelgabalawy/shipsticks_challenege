"""Page Object for Step 1 of the booking flow."""
from pages.base_page import BasePage


class HomePage(BasePage):

    # ==================== ELEMENTS ====================

    # --- Shipping options (landing page) ---

    @property
    def shipment_type_dropdown(self):
        """Dropdown to select trip type (One-way / Round trip)."""
        # nothing was very unique about this element like an id or something clear and easy so I selected a css selector
        return self.page.locator("button[aria-haspopup='listbox']").first

    def shipment_type_option(self, option_text):
        """Option inside the shipment type dropdown."""
        # captured thise element with the role and text because that was the most clear and stable way
        return self.page.get_by_role("option", name=option_text, exact=True)

    @property
    def origin_input(self):
        """Autocomplete input for the origin address."""
        # Place holder text was the best way to capture this element
        return self.page.get_by_placeholder("Where from?")

    @property
    def destination_input(self):
        """Autocomplete input for the destination address."""
        # Place holder text was the best way to capture this element
        return self.page.get_by_placeholder("Where to?")

    @property
    def get_started_button(self):
        """Submit button on the landing page to start the booking."""
        return self.page.get_by_role("button", name="Get started")

    # ==================== ACTIONS ====================

    def go_to_home(self):
        """Navigate to the booking landing page."""
        self.navigate()

    def select_shipment_type(self, shipment_type):
        """Open the trip type dropdown and select the given option."""
        if "-" in shipment_type:
            shipment_type = shipment_type.replace("-", " ")
        self.shipment_type_dropdown.click()
        self.shipment_type_option(shipment_type).click()

    def _fill_address(self, input_locator, address):
        """Shared logic for origin/destination with retry for flaky autocomplete."""
        input_locator.wait_for(state="visible", timeout=10000)

        # Fast attempt — fill triggers autocomplete on most SPAs
        input_locator.fill(address)

        try:
            self.page.get_by_role("option").first.wait_for(timeout=5000)
        except:
            # Slow retry — type char by char to force input events
            input_locator.fill("")
            self.page.wait_for_timeout(500)
            input_locator.type(address, delay=50)
            self.page.get_by_role("option").first.wait_for(timeout=5000)

        # Retry click — autocomplete options can detach/reattach during render
        for _ in range(3):
            try:
                self.page.get_by_role("option").first.click(timeout=3000)
                return
            except:
                self.page.wait_for_timeout(500)

    def enter_origin(self, address):
        """Fill the origin address and select the first autocomplete suggestion."""
        self._fill_address(self.origin_input, address)

    def enter_destination(self, address):
        """Fill the destination address and select the first autocomplete suggestion."""
        self._fill_address(self.destination_input, address)

    def select_origin_n_destination(self, trip_type, origin_add, dest_address):
        """Complete the landing page: origin, destination, trip type, then click Get Started."""
        self.enter_origin(origin_add)
        self.enter_destination(dest_address)
        self.select_shipment_type(trip_type)
        self.get_started_button.click()
