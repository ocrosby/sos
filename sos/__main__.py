"""
This module is the entry point for the application.
"""

from selenium.webdriver.chrome.webdriver import WebDriver

from sos.constants import TURNOUT_URL
from sos.filesystem import write_file
from sos.selenium_webdriver_helpers import (
    create_driver,
    scroll_to_element,
    switch_to_iframe,
    wait_for_clickability,
    wait_for_visibility,
)
from sos.html import beautify_data


def fetch_data(driver: WebDriver, url: str, timeout: int = 20) -> str:
    try:
        # Fetch the page
        driver.get(url)

        absentee_ballots_button_id = "AbsenteeBallots"

        switch_to_iframe(driver, timeout, "Data Hub - Voter Registration")

        wait_for_visibility(driver, timeout, element_id=absentee_ballots_button_id)

        button = scroll_to_element(driver, absentee_ballots_button_id)

        # Wait until the button is clickable
        wait_for_clickability(driver, timeout, element_id=absentee_ballots_button_id)

        button.click()

        # Get the page source
        data = driver.page_source
    finally:
        # Clean up and close the driver
        driver.quit()

    return data


def main():
    # Initialize the WebDriver
    driver = create_driver()

    data = fetch_data(driver, TURNOUT_URL, timeout=20)
    pretty_html = beautify_data(data)
    write_file("output.html", pretty_html)


if __name__ == "__main__":
    main()
