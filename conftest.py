import json
import pytest
from playwright.sync_api import sync_playwright


def load_config():
    with open("config.json", "r") as f:
        return json.load(f)


def pytest_addoption(parser):
    parser.addoption("--record", action="store_true", default=False,
                     help="Record a video of the test execution")


@pytest.fixture(scope="session")
def config():
    return load_config()


@pytest.fixture(scope="session")
def browser(config):
    with sync_playwright() as p:
        browser_type = getattr(p, config["browser"])
        browser = browser_type.launch(headless=config["headless"])
        yield browser
        browser.close()


@pytest.fixture
def page(browser, config, request):
    context_args = {}
    if request.config.getoption("--record"):
        context_args["record_video_dir"] = "videos/"
        context_args["record_video_size"] = {"width": 1280, "height": 720}

    context = browser.new_context(**context_args)
    page = context.new_page()
    page.set_default_timeout(config["timeout"])
    yield page
    context.close()


@pytest.fixture
def test_data(config):
    return config["test_data"]
