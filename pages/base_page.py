"""Base page object — shared helpers for all pages."""
import json


class BasePage:
    def __init__(self, page):
        self.page = page
        with open("config.json", "r") as f:
            self.config = json.load(f)
        self.base_url = self.config["base_url"]

    def navigate(self, path=""):
        self.page.goto(f"{self.base_url}/{path}", wait_until="domcontentloaded")

    def wait_for_element(self, selector, timeout=None):
        self.page.wait_for_selector(selector, timeout=timeout)

    def click(self, selector):
        self.page.click(selector)

    def fill(self, selector, text):
        self.page.fill(selector, text)

    def get_text(self, selector):
        return self.page.text_content(selector)

    def is_visible(self, selector):
        return self.page.is_visible(selector)
