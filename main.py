from time import sleep
from selenium.common.exceptions import NoSuchElementException, TimeoutException
import requests  # Add this line to import the requests module
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from datetime import datetime
import sys
import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium_stealth import stealth
from twocaptcha.solver import TwoCaptcha
import time

sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

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


def jetstarScrape(functionality, flight_type):
    options = Options()
    options.add_argument("start-maximized")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)
    options.add_argument("--headless")  # Runs Chrome in headless mode.

    # pathMac = '/Users/daniel/Downloads/chromedriver-mac-x64/chromedriver'
    # pathWindows = 'C:\\Users\\NZXT\\chromedriver-win64\\chromedriver.exe'
    # Change based on system path to chromedriver.exe

    # Macbook directory
    s = Service('/Users/daniel/Downloads/chromedriver-mac-x64/chromedriver')

    # Windows directory
    # s = Service(pathWindows)

    driver = webdriver.Chrome(service=s, options=options)

    # Apply selenium-stealth settings
    stealth(driver,
            languages=["en-US", "en"],
            vendor="Google Inc.",
            platform="Win32",
            webgl_vendor="Intel Inc.",
            renderer="Intel Iris OpenGL Engine",
            fix_hairline=True,
            )

    url = 'https://www.jetstar.com/au/en/home'
    driver.get(url)
    start_time = time.time()  # Start time before clicking the search button
    # Perform any necessary actions to establish your session
    # Include these cookies in subsequent requests or actions
    wait = WebDriverWait(driver, 20)

    combobox_panels = wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, "comboboxpanel_panel__8Zbd2")))

    # Assuming the departure combobox is the first one and destination is the second one
    departure_combobox = combobox_panels[0]
    destination_combobox = combobox_panels[1]

    departureAirportDropdownXPath = driver.find_element(By.CSS_SELECTOR, '[data-testid="origin"]')
    departureAirportDropdownXPath.click()

    if 'departureAirport' in functionality and functionality['departureAirport'] == 'depSydney':
        sydney_departure_option = departure_combobox.find_element(By.XPATH, ".//div[contains(text(), 'Sydney - SYD')]")
        sydney_departure_option.click()

    elif 'departureAirport' in functionality and functionality['departureAirport'] == 'depMelbourneTullamarine':
        melbourneTullamarine_departure_option = departure_combobox.find_element(By.XPATH,
                                                                                ".//div[contains(text(), 'Melbourne (Tullamarine) - MEL')]")
        melbourneTullamarine_departure_option.click()

    arrivalAirportDropdownXPath = driver.find_element(By.CSS_SELECTOR, '[data-testid="destination"]')
    arrivalAirportDropdownXPath.click()

    if 'arrivalAirport' in functionality and functionality['arrivalAirport'] == 'arrSydney':
        sydney_arrival_option = destination_combobox.find_element(By.XPATH,
                                                                  ".//div[contains(text(), 'Sydney - SYD')]")
        sydney_arrival_option.click()
    elif 'arrivalAirport' in functionality and functionality['arrivalAirport'] == 'arrMelbourneTullamarine':
        melbourneTullamarine_arrival_option = destination_combobox.find_element(By.XPATH,
                                                                                ".//div[contains(text(), 'Melbourne (Tullamarine) - MEL')]")
        melbourneTullamarine_arrival_option.click()

    # Handle one-way flight logic
    if flight_type == 'one-way':
        print("One Way")
        date_picker_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, '.DatesSelector_searchInputWrapper__lQuuI')))
        date_picker_button.click()
        print("CSS Selector Worked")

        journeyRadio = driver.find_elements(By.CSS_SELECTOR, ".radio_label__2GwuZ")

        # Assuming the departure combobox is the first one and destination is the second one
        returnRadio = journeyRadio[0]
        oneWayRadio = journeyRadio[1]

        oneWayRadio.click()

        # Check if 'departureDate' is in the options and not empty
        if 'departureDate' in functionality and functionality['departureDate']:
            desired_date = datetime.strptime(functionality['departureDate'], '%Y-%m-%d')

        datePickerOptions = driver.find_elements(By.CLASS_NAME, "daypicker__caption_label--c-UgT")

        # Assuming the departure combobox is the first one and destination is the second one
        leftMMYY = datePickerOptions[0].text
        rightMMYY = datePickerOptions[1].text

        departure_date_obj = datetime.strptime(functionality['departureDate'], '%Y-%m-%d')
        formatted_date = departure_date_obj.strftime('%B %Y')

        if leftMMYY == formatted_date:
            print("leftMMYY matches the user input date")

        else:
            while leftMMYY != formatted_date:
                print("Current month is " + leftMMYY + ". Clicking next month button...")

                # Click the next month button
                nextMonthButtonXPath = driver.find_element(By.XPATH,
                                                           '//*[@id="popoverContent"]/div/div/div/div[2]/div[2]/div/div[2]/div/div/button')
                nextMonthButtonXPath.click()

                # Wait for the text of the datePickerOptions to be updated to the new month
                try:
                    wait.until_not(
                        EC.text_to_be_present_in_element((By.CLASS_NAME, "daypicker__caption_label--c-UgT"), leftMMYY))
                except TimeoutException:
                    print("Timed out waiting for the month to update after clicking next month button.")
                    break  # Exit the loop if the month doesn't update

                # Re-find the element to get the updated text after the page content has changed
                datePickerOptions = driver.find_elements(By.CLASS_NAME, "daypicker__caption_label--c-UgT")
                leftMMYY = datePickerOptions[0].text
                print("Updated month is " + leftMMYY)

        # Add date selection logic
        dayPickerOptions = driver.find_elements(By.CLASS_NAME, "daypicker__tbody--UL-3t")
        leftDaySelectBlock = dayPickerOptions[0]
        rightDaySelectBlock = dayPickerOptions[1]

        fullDepartureObj = datetime.strptime(functionality['departureDate'], '%Y-%m-%d')
        formatted_date_id = fullDepartureObj.strftime('%d-%m-%Y')  # Format date to match ID format

        buttonsInLeftBlock = leftDaySelectBlock.find_elements(By.CSS_SELECTOR,
                                                              '.daypicker__button_reset--inqB7.daypicker__button--ayiU1.daypicker__day--FYuDG')

        for WebElement in buttonsInLeftBlock:
            fullDepartureObj = datetime.strptime(functionality['departureDate'], '%Y-%m-%d')

            # Format the date to match the expected 'dd-mm-yyyy' ID format, including leading zeros
            formatted_date_id = fullDepartureObj.strftime('%d-%m-%Y')
            element_id = WebElement.get_attribute('id')
            if element_id == formatted_date_id:
                print(f"Found the matching date button: {formatted_date_id}")
                WebElement.click()  # Click the button if it's the right date
                break  # Exit the loop since we've found the correct date button
            else:
                print(f"Current element ID: {element_id} does not match {formatted_date_id}")

        submitPATH = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR,
                                        '.button_base__fanGW.button_variant__Ru2LZ.button_brand__LIV-9.button_size-small__B0Rtz.button_isRounded__5JCYx')))
        submitPATH.click()

        searchButtonPATH = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, '[data-testid="button-search-jcl"]')))
        searchButtonPATH.click()

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

    # Replace 'YOUR_2CAPTCHA_API_KEY' with your actual 2Captcha API key
    api_key = 'c4d24eaca65b2982a0710f09c28d8dbe'

    solver = TwoCaptcha(api_key)
    try:
        captcha_iframe = driver.find_element(By.ID, 'sec-cpt-if')
        driver.switch_to.frame(captcha_iframe)
        print("Switched to iframe containing CAPTCHA")
        checkbox = driver.find_element(By.ID, 'sec-if-cpt-container')
        checkbox.click()

        try:
            result = solver.recaptcha(
                sitekey='6Ld-zbkUAAAAAB_gkIieRFcyI4V93OJwX0GuUrlU',
                url='https://booking.jetstar.com/au/en/booking/select-flights'
            )
            print('solved: ' + str(result))

            # Now find and interact with the CAPTCHA response textarea
            # Switch to the iframe that contains the CAPTCHA

            # The element might be hidden, ensure that it is visible

            # Submit the CAPTCHA response value into the textarea
            recaptcha_response_textarea = driver.find_element(By.ID, 'g-recaptcha-response')

            driver.execute_script("arguments[0].style.display = 'block';", recaptcha_response_textarea)
            driver.execute_script(f"document.getElementById('g-recaptcha-response').value='{result['code']}';")
            # Trigger any necessary events after setting the value
            driver.execute_script("document.getElementById('g-recaptcha-response').dispatchEvent(new Event('change'));")

            driver.execute_script(f"verifyAkReCaptcha('{result['code']}');")
            print("Complete")

            # Switch back to the main content
            driver.switch_to.default_content()
            end_time = time.time()
            total_time = end_time - start_time
            print(f"Total execution time: {total_time} seconds")
            sleep(5)

            # Don't forget to switch back to the default content when done
            # Failed to solve CAPTCHA: Message: no such element: Unable to locate element: {"method":"css selector","selector":"[id="g-recaptcha-response"]"}

        except Exception as e:
            print('Failed to solve CAPTCHA:', e)
            sleep(1000)

    except Exception as t:
        print("No Captcha Found: " + e)
        pass


def qantasScrape(functionality, flight_type):
    options = Options()
    options.add_argument("start-maximized")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)

    # pathMac = '/Users/daniel/Downloads/chromedriver-mac-x64/chromedriver'
    # pathWindows = 'C:\\Users\\NZXT\\chromedriver-win64\\chromedriver.exe'
    # Change based on system path to chromedriver.exe

    # Macbook directory
    s = Service('/Users/daniel/Downloads/chromedriver-mac-x64/chromedriver')

    # Windows directory
    # s = Service(pathWindows)

    driver = webdriver.Chrome(service=s, options=options)

    # Apply selenium-stealth settings
    stealth(driver,
            languages=["en-US", "en"],
            vendor="Google Inc.",
            platform="Win32",
            webgl_vendor="Intel Inc.",
            renderer="Intel Iris OpenGL Engine",
            fix_hairline=True,
            )

    url = 'https://www.qantas.com/au/en.html'
    driver.get(url)
    start_time = time.time()  # Start time before clicking the search button
    # Perform any necessary actions to establish your session
    # Include these cookies in subsequent requests or actions
    wait = WebDriverWait(driver, 10)

    airport_code_mapping = {
        'depSydney': 'SYD',
        'depMelbourneTullamarine': 'MEL',
        # Add more mappings as needed
    }

    menuOpen = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, '.css-gn7407-LargeButton')))
    menuOpen.click()

    originAirportPath = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, '.css-shnplr-runway-dialog-button__value--large-LargeButton')))
    originAirportPath.click()

    if 'departureAirport' in functionality and 'arrivalAirport' in functionality:
        # Define a mapping from the form value to the airport code

        dep_value = functionality['departureAirport']
        origin_airport_code = airport_code_mapping.get(dep_value, 'Unknown')  # Get the airport code, or 'Unknown' if not found

        text_area = driver.find_element(By.CSS_SELECTOR, ".css-1mu1mk2")  # Replace "textAreaId" with the actual ID or locator
        text_area.clear()  # It's a good practice to clear the field first, in case there is any pre-filled data
        text_area.send_keys(origin_airport_code)

        departureAirportPath = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, 'css-kx5i2d-runway-popup-field__placeholder-LargeButton')))
        departureAirportPath.click()

        arr_value = functionality['arrivalAirport']
        departure_airport_code = airport_code_mapping.get(arr_value, 'Unknown')  # Get the airport code, or 'Unknown' if not found

        text_area = driver.find_element(By.CSS_SELECTOR, ".css-1mu1mk2")  # Replace "textAreaId" with the actual ID or locator
        text_area.clear()  # It's a good practice to clear the field first, in case there is any pre-filled data
        text_area.send_keys(departure_airport_code)



    sleep(10)


def clearVariables():
    lst_prices.clear()
    lst_airline.clear()
    lst_departure.clear()


if __name__ == "__main__":
    print("Hello World")
