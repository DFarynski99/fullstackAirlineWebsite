from time import sleep
from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.common.exceptions import NoSuchElementException
import requests  # Add this line to import the requests module
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from datetime import datetime

lst_prices = []
lst_airline = []
lst_departure = []


def notify_ifttt(price):
    event_name = 'price_drop'
    key = 'o68zKbvAHahsn_vcuM8O_PHpKoBIN_aCzS0e22_wHBd'  # Replace with your IFTTT Webhooks key
    url = f'https://maker.ifttt.com/trigger/price-drop/with/key/{key}'

    # Data to pass to the email body, you can add more with Value2, Value3 etc.
    data = {'value1': lst_prices, 'value2': lst_airline, 'value3': lst_departure}
    response = requests.post(url, json=data)
    print(f'Notification sent for price drop: {lst_prices}')


def check_prices_and_notify(lst_prices):
    for price_str in lst_prices:
        # Clean the price string and convert it to a float
        price_value = float(price_str.replace('$', ''))

        # Check if the price is below $200
        if price_value < 200:
            print(f"Price dropped to ${price_value}, sending notification...")
            notify_ifttt(f'$ {price_value}')
            print("")
        else:
            print(f"Price is ${price_value}, no notification sent.")
            print("")


def scraperLogic():
    # Setup Chrome options
    chrome_options = ChromeOptions()
    chrome_options.headless = True  # Enable headless mode

    # Initialize the Remote WebDriver
    driver = webdriver.Remote(
        command_executor='http://localhost:4444/wd/hub',
        options=chrome_options  # Specify ChromeOptions here
    )

    url = 'https://www.skyscanner.com.au/transport/flights/bne/per/240419/?adults=1&adultsv2=1&airlines=-31940,-31876,-32646,-32166,-32076,-31694,multiple&cabinclass=economy&children=0&childrenv2=&destinationentityid=27545934&duration=1080&inboundaltsenabled=false&infants=0&originentityid=27539494&outboundaltsenabled=false&ref=home&rtn=0&stops=!oneStop,!twoPlusStops'

    driver.get(url)

    try:
        # Adjusted for Selenium 4: Using By.CLASS_NAME to specify the search criterion
        captcha_element = driver.find_element(By.CLASS_NAME, "g-recaptcha")
        print("CAPTCHA detected.")
    except NoSuchElementException:
        print("No CAPTCHA detected.")

    # Checking for specific text indicating a CAPTCHA challenge
    page_source = driver.page_source.lower()
    if "captcha" in page_source or "are you a robot?" in page_source:
        print("CAPTCHA challenge text found on the page.")

    # Check for unexpected page titles or URLs that might indicate a CAPTCHA
    if "CAPTCHA" in driver.title:
        print("Page title suggests a CAPTCHA is present.")

    print("Waiting 25 seconds for all elements to load")
    sleep(25)  # Waits for the page to load. Consider using WebDriver wait conditions instead for better reliability.

    loadMoreButtonXPath = "//button[@class='BpkButton_bpk-button__YzJlY BpkButton_bpk-button--secondary__OGE0O']"

    try:
        # Try to find and click the "Load More" button
        load_more_button = driver.find_element(By.XPATH, loadMoreButtonXPath)
        driver.execute_script("arguments[0].click();", load_more_button)

    except NoSuchElementException:
        # If the button is not found, skip clicking and proceed
        print("Load More button not found, proceeding without clicking.")

    print("Waiting 5 seconds for all elements to load")
    sleep(5)  # Waits for the page to load. Consider using WebDriver wait conditions instead for better reliability.

    # Use find_elements to get a list of elements
    flight_rows = driver.find_elements(By.XPATH, '//div[@class="EcoTicketWrapper_itineraryContainer__ZWE4O"]')
    flight_rows_emissions = driver.find_elements(By.XPATH, '//div[@class="EcoTicketWrapper_ecoContainer__YjNmN"]')

    for WebElement in flight_rows:
        elementHTML = WebElement.get_attribute('outerHTML')
        elementSoup = BeautifulSoup(elementHTML, 'html.parser')

        # price
        temp_price = elementSoup.find("div", {"class": "Price_mainPriceContainer__MDM3O"})
        if temp_price:  # Check if the price element is found
            price = temp_price.find("span", {"class": "BpkText_bpk-text__MWZkY BpkText_bpk-text--lg__NjNhN"})
            if price:  # Check if the span containing the price is found
                lst_prices.append(price.text)

    for WebElement in flight_rows:
        elementHTML = WebElement.get_attribute('outerHTML')
        elementSoup = BeautifulSoup(elementHTML, 'html.parser')

        # Attempt to find the airline name within the current WebElement
        temp_airline = elementSoup.find("div", {"class": "FlightsTicketBody_container__OTEwN"})
        if temp_airline:
            airline = temp_airline.find("span", {"class": "BpkText_bpk-text__MWZkY BpkText_bpk-text--xs__ZDJmY"})
            if airline:
                lst_airline.append(
                    airline.text.strip())  # Added strip() to remove potential leading/trailing whitespace

    for WebElement in flight_rows:
        elementHTML = WebElement.get_attribute('outerHTML')
        elementSoup = BeautifulSoup(elementHTML, 'html.parser')

        # Attempt to find the airline name within the current WebElement
        temp_departure = elementSoup.find("div", {"class": "LegInfo_routePartialDepart__NzEwY"})
        if temp_departure:
            departure = temp_departure.find("span",
                                            {"class": "BpkText_bpk-text__MWZkY BpkText_bpk-text--subheading__NzkwO"})
            if departure:
                lst_departure.append(
                    departure.text.strip())  # Added strip() to remove potential leading/trailing whitespace

    for WebElement in flight_rows_emissions:
        elementHTML = WebElement.get_attribute('outerHTML')
        elementSoup = BeautifulSoup(elementHTML, 'html.parser')

        temp_price = elementSoup.find("div", {"class": "Price_mainPriceContainer__MDM3O"})
        if temp_price:  # Check if the price element is found
            price = temp_price.find("span", {"class": "BpkText_bpk-text__MWZkY BpkText_bpk-text--lg__NjNhN"})
            if price:  # Check if the span containing the price is found
                lst_prices.append(price.text)

    for WebElement in flight_rows_emissions:
        elementHTML = WebElement.get_attribute('outerHTML')
        elementSoup = BeautifulSoup(elementHTML, 'html.parser')

        # Attempt to find the airline name within the current WebElement
        temp_airline = elementSoup.find("div", {"class": "FlightsTicketBody_container__OTEwN"})
        if temp_airline:
            airline = temp_airline.find("span", {"class": "BpkText_bpk-text__MWZkY BpkText_bpk-text--xs__ZDJmY"})
            if airline:
                lst_airline.append(
                    airline.text.strip())  # Added strip() to remove potential leading/trailing whitespace

    for WebElement in flight_rows_emissions:
        elementHTML = WebElement.get_attribute('outerHTML')
        elementSoup = BeautifulSoup(elementHTML, 'html.parser')

        # Attempt to find the airline name within the current WebElement
        temp_departure = elementSoup.find("div", {"class": "LegInfo_routePartialArrive__Y2U1N"})
        if temp_departure:
            departure = temp_departure.find("span",
                                            {"class": "BpkText_bpk-text__MWZkY BpkText_bpk-text--subheading__NzkwO"})
            if departure:
                lst_departure.append(
                    departure.text.strip())  # Added strip() to remove potential leading/trailing whitespace

    print("These are the flight matching your search filters:")
    print("--------------------------------------------------")
    for i in range(len(lst_prices)):
        print(lst_prices[i] + " - " + lst_airline[i] + " - " + lst_departure[i])
    print("")
    driver.quit()  # Ensure the driver is quit even if an error occurs


def jetstarScrape(options, flight_type):
    driver = webdriver.Chrome()
    url = 'https://www.jetstar.com/au/en/home'
    driver.get(url)

    print("Sleeping for 8 seconds to let all elements load")
    sleep(4)

    combobox_panels = driver.find_elements(By.CLASS_NAME, "comboboxpanel_panel__8Zbd2")

    # Assuming the departure combobox is the first one and destination is the second one
    departure_combobox = combobox_panels[0]
    destination_combobox = combobox_panels[1]
    departureAirportDropdownXPath = '//*[@id="flockSearch"]/form/div[1]'
    driver.find_element(By.XPATH, departureAirportDropdownXPath).click()
    sleep(2)

    if 'departureAirport' in options and options['departureAirport'] == 'depSydney':
        sydney_departure_option = departure_combobox.find_element(By.XPATH, ".//div[contains(text(), 'Sydney - SYD')]")
        sydney_departure_option.click()
        sleep(2)

    elif 'departureAirport' in options and options['departureAirport'] == 'depMelbourneTullamarine':
        melbourneTullamarine_departure_option = departure_combobox.find_element(By.XPATH,
                                                                                ".//div[contains(text(), 'Melbourne (Tullamarine) - MEL')]")
        melbourneTullamarine_departure_option.click()
        sleep(2)

    arrivalAirportDropdownXPath = '//*[@id="flockSearch"]/form/div[2]'
    driver.find_element(By.XPATH, arrivalAirportDropdownXPath).click()
    sleep(2)

    if 'arrivalAirport' in options and options['arrivalAirport'] == 'arrSydney':
        sydney_arrival_option = destination_combobox.find_element(By.XPATH,
                                                                  ".//div[contains(text(), 'Sydney - SYD')]")
        sydney_arrival_option.click()
        sleep(2)
    elif 'arrivalAirport' in options and options['arrivalAirport'] == 'arrMelbourneTullamarine':
        melbourneTullamarine_arrival_option = destination_combobox.find_element(By.XPATH,
                                                                                ".//div[contains(text(), 'Melbourne (Tullamarine) - MEL')]")
        melbourneTullamarine_arrival_option.click()
        sleep(2)

    # Handle one-way flight logic
    if flight_type == 'one-way':
        print("One Way")
        date_picker_button = driver.find_element(By.XPATH, '//*[@id="flockSearch"]/form/div[3]/div/div[1]')
        date_picker_button.click()

        # Check if 'departureDate' is in the options and not empty
        if 'departureDate' in options and options['departureDate']:
            desired_date = datetime.strptime(options['departureDate'], '%Y-%m-%d')
            wait = WebDriverWait(driver, 10)

        # Scrape the Month Year on Jetstar and hardcode March 2024 === 2024/03 so on so forth,
        # Compare to YYYY/MM provided by user on front end
        # IF YYYY/MM > scraped date, click back a month, ELIF YYYY/MM < scraped date, click forward a month, ELSE stay
        # Then code logic for finding and clicking appropriate date
        pass

    # Handle return flight logic
    elif flight_type == 'return':
        # Your logic for return flights
        # In addition to the one-way logic, you will also select the return date
        print("Return")
        pass


def clearVariables():
    lst_prices.clear()
    lst_airline.clear()
    lst_departure.clear()


def perform_scrape():
    clearVariables()  # Clear previous data
    scraperLogic()  # Perform scraping
    check_prices_and_notify(lst_prices)
    # Format your results here
    results = list(zip(lst_prices, lst_airline, lst_departure))
    return results


if __name__ == "__main__":
    perform_scrape()
