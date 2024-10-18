from sos.constants import TURNOUT_URL

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager


def fetch_data(url):
    # Set up headless Chrome options
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")

    # Initialize the WebDriver
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)

    try:
        # Fetch the page
        driver.get(url)

        # Get the page source
        data = driver.page_source
    finally:
        # Clean up and close the driver
        driver.quit()

    return data


def main():
    data = fetch_data(TURNOUT_URL)
    print(data)


if __name__ == "__main__":
    main()
