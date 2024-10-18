"""
This module contains helper functions for the Selenium WebDriver.
"""

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager


def create_driver(headless: bool = True) -> WebDriver:
    """
    Create a Chrome WebDriver instance.

    :param headless:
    :return:
    """
    chrome_args = ["--disable-gpu", "--no-sandbox", "--disable-dev-shm-usage"]
    chrome_options = create_chrome_options(headless=headless, arguments=chrome_args)
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)
    return driver


def scroll_to_element(driver: WebDriver, element_id: str) -> WebElement:
    """
    Scroll to the element by its ID.

    :param driver: the WebDriver instance
    :param element_id: the element ID to scroll to
    :return: the web element
    """
    # Scroll the button into view
    button: WebElement = find_element_by_id(driver=driver, element_id=element_id)
    execute_script(
        driver=driver, script="arguments[0].scrollIntoView(true);", web_element=button
    )
    return button


def execute_script(driver: WebDriver, script: str, web_element: WebElement) -> None:
    """
    Execute Javascript on the web element.

    :param driver: the WebDriver instance
    :param script: the script to execute
    :param web_element: the web element to execute the script on
    :return: None
    """
    driver.execute_script(script, web_element)


def create_chrome_options(headless: bool, arguments: list[str]) -> Options:
    """
    Create Chrome options with the given arguments.

    :param headless: a boolean flag to run Chrome in headless
    :param arguments: a list of arguments to pass to Chrome
    :return: options for Chrome
    """
    options = Options()

    if headless:
        options.add_argument("--headless")

    for argument in arguments:
        options.add_argument(argument)

    return options


def find_element_by_id(driver: WebDriver, element_id: str) -> WebElement:
    button = driver.find_element(By.ID, value=element_id)
    return button


def wait_for_clickability(driver: WebDriver, timeout: int, element_id: str) -> None:
    """
    Wait for the element to be clickable.

    :param driver: the WebDriver instance
    :param timeout: the timeout in seconds
    :param element_id: the element ID to wait for
    :return: None
    """
    WebDriverWait(driver, timeout=timeout).until(
        EC.element_to_be_clickable((By.ID, element_id))
    )


def wait_for_visibility(driver: WebDriver, timeout: int, element_id: str) -> None:
    """
    Wait for the element to be visible.

    :param driver: the WebDriver instance
    :param timeout: the timeout in seconds
    :param element_id: the element ID to wait for
    :return: None
    """
    WebDriverWait(driver, timeout=timeout).until(
        EC.visibility_of_element_located((By.ID, element_id))
    )


def switch_to_iframe(driver: WebDriver, timeout: int, title: str) -> None:
    """
    Switch to the iframe by its title.

    :param driver: the WebDriver instance
    :param timeout: the timeout in seconds
    :param title: the title of the iframe
    :return: None
    """
    # Switch to the iframe by its title
    WebDriverWait(driver, timeout=timeout).until(
        EC.frame_to_be_available_and_switch_to_it(
            (By.XPATH, f"//iframe[@title='{title}']")
        )
    )
