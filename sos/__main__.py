from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
from sos.constants import TURNOUT_URL


def fetch_data(url):
    # Set up headless Chrome options
    chrome_options = Options()
    # chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")

    # Initialize the WebDriver
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)

    try:
        # Fetch the page
        driver.get(url)

        # Switch to the iframe by its title
        WebDriverWait(driver, 20).until(
            EC.frame_to_be_available_and_switch_to_it((By.XPATH, "//iframe[@title='Data Hub - Voter Registration']"))
        )

        # Wait until the button is visible
        WebDriverWait(driver, 20).until(
            EC.visibility_of_element_located((By.ID, "AbsenteeBallots"))
        )

        # Scroll the button into view
        button = driver.find_element(By.ID, "AbsenteeBallots")
        driver.execute_script("arguments[0].scrollIntoView(true);", button)

        # Wait until the button is clickable
        WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.ID, "AbsenteeBallots"))
        )

        button.click()

        # Get the page source
        data = driver.page_source
    finally:
        # Clean up and close the driver
        driver.quit()

    return data


def main():
    data = fetch_data(TURNOUT_URL)
    soup = BeautifulSoup(data, "html.parser")
    pretty_html = soup.prettify()
    with open("output.html", "w", encoding="utf-8") as file:
        file.write(pretty_html)


if __name__ == "__main__":
    main()
