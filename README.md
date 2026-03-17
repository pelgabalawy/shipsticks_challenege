# ShipSticks Booking Flow — Automated Tests

End-to-end UI tests for the ShipSticks booking flow, built with **Playwright** and **pytest**.

## Prerequisites

- Python 3.10+
- pip

## Setup

1. Create and activate a virtual environment:

   ```bash
   python -m venv .venv
   source .venv/bin/activate        # macOS / Linux
   .venv\Scripts\activate           # Windows
   ```

2. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. Install Playwright browsers:

   ```bash
   playwright install
   ```

## Configuration

Test cases rely on `config.json` as the single source for both environment settings and test data. This file must be present in the project root before running any tests.

| Key              | Description                                      |
|------------------|--------------------------------------------------|
| `base_url`       | Target environment URL                           |
| `browser`        | Browser engine (`chromium`, `firefox`, `webkit`)  |
| `headless`       | Run without a visible browser window (`true/false`) |
| `timeout`        | Default timeout in milliseconds                  |
| `test_data`      | Test input data (addresses, item, dates, etc.)   |

Example `config.json` (This is fake data!):

```json
{
  "base_url": "https://your-environment-url.com",
  "browser": "chromium",
  "headless": false,
  "timeout": 30000,
  "test_data": {
    "shipment_type": "One-way",
    "item": "Golf Bag (Standard)",
    "origin": "123 Example St, City, ST, USA",
    "destination": "456 Sample Ave, Town, ST, USA",
    "service_level": "Ground",
    "delivery_date": "Wednesday, January 1, 2030"
  }
}
```

To run tests with different data, just update the values in `config.json` before executing.

## Running Tests

Run all tests:

```bash
pytest
```

Run a specific test:

```bash
pytest tests/test_booking_step1.py
```

Run with verbose output:

```bash
pytest -v
```

## Recording Video

To record a video of the test execution, add the `--record` flag:

```bash
pytest --record
```

Videos are saved to the `videos/` directory in the project root. Each browser context gets its own `.webm` file.

To record a specific test:

```bash
pytest tests/test_booking_step1.py --record
```

> Without the `--record` flag, no video is captured — recording is fully on-demand.

## Project Structure

```
├── config.json              # Test configuration and data
├── conftest.py              # Pytest fixtures (browser, page, video recording)
├── pages/
│   ├── base_page.py         # Base page object
│   ├── home_page.py         # Home page actions
│   └── booking_page.py       # Booking Step 1 page actions
├── tests/
│   └── test_booking_step1.py# Booking Step 1 happy-path test
├── test_plan.txt            # Manual test plan reference
└── requirements.txt         # Python dependencies
```
