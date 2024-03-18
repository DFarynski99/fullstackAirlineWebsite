import os
import sys
import time
from datetime import datetime
from time import sleep
import undetected_chromedriver as uc
from selenium import webdriver
from selenium.common.exceptions import StaleElementReferenceException, WebDriverException, NoSuchElementException
from selenium.common.exceptions import TimeoutException, ElementClickInterceptedException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium_stealth import stealth
from twocaptcha.solver import TwoCaptcha

sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))


def jetstarScrape(functionality, flight_type):
    options = Options()
    options.add_argument("start-maximized")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)
    # options.add_argument("--headless")  # Runs Chrome in headless mode.

    # pathMac = '/Users/daniel/Downloads/chromedriver-mac-x64/chromedriver'
    # pathWindows = 'C:\\Users\\NZXT\\chromedriver-win64\\chromedriver.exe'
    # Change based on system path to chromedriver.exe

    # Macbook directory
    s = Service('C:\\Users\\NZXT\\chromedriver-win64\\chromedriver.exe')

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
        oneWayRadio = journeyRadio[1]

        oneWayRadio.click()

        datePickerOptions = driver.find_elements(By.CLASS_NAME, "daypicker__caption_label--c-UgT")

        # Assuming the departure combobox is the first one and destination is the second one
        leftMMYY = datePickerOptions[0].text

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

    # Assuming `driver` is your WebDriver instance
    allFlightCards = driver.find_elements(By.CSS_SELECTOR, '.flight-card-wrapper.js-fare-row')
    # Calculate half the size of flightCards
    half_size = len(allFlightCards) // 2
    # This is the first half of the allFlightCards
    flightCards = allFlightCards[:half_size]
    results = []
    for card in flightCards:
        departureTime = card.find_element(By.CSS_SELECTOR, '.itinerary-info__time.js-departure-time.departuretime').text
        departureAirport = card.find_element(By.CSS_SELECTOR, '.itinerary-info__airport').text

        arrivalTime = card.find_elements(By.CSS_SELECTOR, '.itinerary-info__time')
        arrivalAirport = card.find_elements(By.CSS_SELECTOR, '.itinerary-info__airport')

        try:
            priceElement = card.find_element(By.CSS_SELECTOR, '.price-wrapper.pricepoint-wrapper.pricepoint-wrapper--orange')
            priceSymbol = priceElement.find_element(By.CSS_SELECTOR, '.pricepoint__symbol')
            priceNumber = priceElement.find_element(By.CSS_SELECTOR, '.js-price.pricepoint__middle')
            completePrice = priceSymbol.text + priceNumber.text
        except NoSuchElementException:
            completePrice = "Sold Out"

        flight_details = {
            'origin_airport': departureAirport,
            'arrival_airport': arrivalAirport[1].text,
            'departure_time': departureTime,
            'arrival_time': arrivalTime[1].text,
            'economy_price': completePrice,
        }
        results.append(flight_details)

    print(results)
    driver.quit()
    return results


def qantasScrape(functionality, flight_type):
    options = uc.ChromeOptions()
    options.add_argument("--start-maximized")  # Open the browser in maximized mode

    driver = uc.Chrome(options=options)

    url = 'https://www.qantas.com/au/en.html'
    driver.get(url)
    driver.maximize_window()
    start_time = time.time()  # Start time before clicking the search button
    # Perform any necessary actions to establish your session
    # Include these cookies in subsequent requests or actions
    wait = WebDriverWait(driver, 10)

    airport_code_mapping = {
        'depSydney': 'SYD',
        'depMelbourneTullamarine': 'MEL',
        'arrSydney': 'SYD',
        'arrMelbourneTullamarine': 'MEL'
        # Add more mappings as needed
    }

    menuOpen = WebDriverWait(driver, 30).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, '.css-gn7407-LargeButton')))
    menuOpen.click()

    def click_with_retry(driver, selector, retries=5, delay=5, scroll_by=75):
        """Attempts to click an element, with retries and a delay between attempts."""
        for attempt in range(retries):
            try:
                # Wait for the element to be clickable
                element = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, selector)))
                # Try clicking the element
                element.click()
                print("Click successful")
                return
            except ElementClickInterceptedException:
                print(f"Click intercepted, attempt {attempt + 1} of {retries}")
                if attempt > 0:
                    scroll_element_into_view(driver, element, scroll_by)
                # Wait for a bit before trying again
                time.sleep(delay)
        raise Exception("Failed to click the element after several retries")

    # If only a flight 'there' date was chosen, a return flight date was not selected
    if flight_type == 'one-way':
        # css-g0vn4r-DropdownMenu-DropdownMenu-overrideClassName-ButtonBase-ButtonBase-css
        onewayDropdown = WebDriverWait(driver, 30).until(
            EC.element_to_be_clickable(
                (By.CSS_SELECTOR, '.css-g0vn4r-DropdownMenu-DropdownMenu-overrideClassName-ButtonBase-ButtonBase-css')))
        try:
            onewayDropdown.click()
        except Exception as e:
            print(e)
            driver.execute_script("arguments[0].click();", onewayDropdown)
        sleep(1)
        one_way_selector = '.css-sgdso3-runway-dropdown__menu-item'
        try:
            click_with_retry(driver, one_way_selector)
        except Exception as e:
            print(e)
            dateSelectFail = True
            print("dateSelectFail is flagged as True")
        sleep(2)

    # Else means if the flight is a return flight
    else:
        pass

    if 'departureAirport' in functionality and 'arrivalAirport' in functionality:
        # Define a mapping from the form value to the airport code
        originAirportPath = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, '.css-shnplr-runway-dialog-button__value--large-LargeButton')))
        originAirportPath.click()

        dep_value = functionality['departureAirport']
        origin_airport_code = airport_code_mapping.get(dep_value,
                                                       'Unknown')  # Get the airport code, or 'Unknown' if not found

        text_area = driver.find_element(By.CSS_SELECTOR,
                                        ".css-1mu1mk2")  # Replace "textAreaId" with the actual ID or locator
        text_area.clear()  # It's a good practice to clear the field first, in case there is any pre-filled data
        text_area.send_keys(origin_airport_code)

        print("Before origin_airport_codes")
        sleep(3)
        origin_airport_codes = driver.find_elements(By.CLASS_NAME, 'css-p8i965')
        print(origin_airport_codes)

        # Iterate through all fetched elements
        for airport_code_element in origin_airport_codes:
            # Get the text of the current element
            airport_code_text = airport_code_element.text

            # Check if the text matches the origin_airport_code
            if airport_code_text == origin_airport_code:
                print("Match found: " + airport_code_text + " = " + origin_airport_code)
                # If a match is found, you might want to break out of the loop or perform some action
                airport_code_element.click()
                break
            else:
                print("Did not work: " + airport_code_text + " : " + origin_airport_code)

        sleep(1)

        arrivalAirportPathArray = wait.until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".css-1oltvto-runway-popup-field__button")))

        # Assuming the departure combobox is the first one and destination is the second one
        origin_box = arrivalAirportPathArray[0]
        arrival_box = arrivalAirportPathArray[1]

        arrival_box.click()

        arr_value = functionality['arrivalAirport']
        arrival_airport_code = airport_code_mapping.get(arr_value,
                                                        'Unknown')  # Get the airport code, or 'Unknown' if not found

        text_area = driver.find_element(By.CSS_SELECTOR,
                                        ".css-1mu1mk2")  # Replace "textAreaId" with the actual ID or locator
        text_area.clear()  # It's a good practice to clear the field first, in case there is any pre-filled data
        text_area.send_keys(arrival_airport_code)

        print("Before arrival_airport_codes")
        sleep(2)
        arrival_airport_codes = driver.find_elements(By.CLASS_NAME, 'css-p8i965')

        # Iterate through all fetched elements
        for airport_code_element_arr in arrival_airport_codes:
            # Get the text of the current element
            airport_code_text_arr = airport_code_element_arr.text

            # Check if the text matches the origin_airport_code
            if airport_code_text_arr == arrival_airport_code:
                print("Match found: " + airport_code_text_arr + " = " + arrival_airport_code)
                # If a match is found, you might want to break out of the loop or perform some action
                airport_code_element_arr.click()
                break
            else:
                print("Did not work: " + airport_code_text_arr + " : " + arrival_airport_code)

    # While loop, while user input Month Year is not found, keep iterating and generating new elements

    dateSelectorButton = '.css-5xbxpx-runway-popup-field__button'
    try:
        click_with_retry(driver, dateSelectorButton)
    except Exception as e:
        print(e)
        dateSelectFail = True
        print("dateSelectFail is flagged as True")

    scrollable_calendar = driver.find_element(By.XPATH, '/html/body/div[15]/div[2]/div/div[3]/div')
    # Now, execute a script to scroll to the bottom of this div
    driver.execute_script('arguments[0].scrollTo(0, arguments[0].scrollHeight)', scrollable_calendar)

    departure_date_obj = datetime.strptime(functionality['departureDate'], '%Y-%m-%d')
    formatted_date = departure_date_obj.strftime('%B %Y')  # Updated to include year in the format

    month_year_found = False

    while not month_year_found:
        try:
            calendarMain = driver.find_elements(By.CLASS_NAME, 'css-fls1na-Month')
            for month_element in calendarMain:
                # Attempt to get the parent element
                parent_element = month_element.find_element(By.XPATH, "..")
                element_text = ' '.join(parent_element.text.split())

                if formatted_date == element_text:
                    print("Match has been found: " + formatted_date + " : " + element_text)
                    month_year_found = True
                    break
        except StaleElementReferenceException:
            # If caught, this will go back to the start of the while loop and try to find the elements again
            # Search only goes till February 2025, if user input is past this, then this will be triggered
            # Need better handling of this, such as blocking the option to choose date past February 2025
            continue

        if not month_year_found:
            driver.execute_script('arguments[0].scrollTo(0, arguments[0].scrollHeight)', scrollable_calendar)

    # 2024-03-24

    # Find and then click the date element
    dateFollowingButtonFormat = datetime.strptime(functionality['departureDate'], '%Y-%m-%d')
    formatted_date = dateFollowingButtonFormat.strftime('%Y-%m-%d')
    print(formatted_date)

    def scroll_element_into_view(driver, element, scroll_by):
        """Scrolls the page a bit to bring the element into a better view."""
        # You can adjust this as necessary. For example, to scroll down:
        driver.execute_script(f"window.scrollBy(0, {scroll_by});")
        # Alternatively, to scroll the element into the center of the view:
        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", element)
        print(f"Scrolled the page by {scroll_by} pixels")

    formatted_date_selector = f'[data-testid="{formatted_date}"]'

    def try_click_date_and_confirm(driver, formatted_date_selector, max_attempts=3):
        attempts = 0
        while attempts < max_attempts:
            try:
                # Attempt to click the date
                click_with_retry(driver, formatted_date_selector)

                # Check if the confirm button is present and clickable
                dateConfirmButton = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, '[data-testid="dialogConfirmation"]')))
                dateConfirmButton.click()

                print("Date selected and confirmed successfully.")
                return  # Exit the function as we've succeeded
            except TimeoutException:
                # If the confirm button wasn't found or wasn't clickable, increment the attempt counter
                print(f"Attempt {attempts + 1} failed; confirm button not found or not clickable.")
                attempts += 1
            except Exception as e:
                print(e)
                print("Unexpected error, aborting.")
                break  # Exit the loop on unexpected errors

        print("Failed to select and confirm date after several attempts.")

    # Usage example
    try_click_date_and_confirm(driver, formatted_date_selector)

    # Search flights button after all selections are made
    searchFlightsButton = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR,
                                    '.css-hbhwmh-baseStyles-baseStyles-baseStyles-solidStyles-solidStyles-solidStyles-Button')))
    searchFlightsButton.click()
    print("Search Flights Button (CSS) Clicked")


    WebDriverWait(driver, 40).until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR, '.list-of-flights__item.ng-star-inserted'))
    )

    loadMoreButton = driver.find_element(By.CSS_SELECTOR,
                                         '.btn.btn-secondary.e2e-show-more-flights-0.show-more-btn.ng-star-inserted')

    try:
        # Try to find the button by its selector
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        sleep(2)
        # If found, click the button
        driver.execute_script("arguments[0].click();", loadMoreButton)
    except NoSuchElementException:
        # If the button does not exist, skip the block
        pass

    WebDriverWait(driver, 40).until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR, '.list-of-flights__item.ng-star-inserted'))
    )

    flightCards = driver.find_elements(By.CSS_SELECTOR, '.list-of-flights__item.ng-star-inserted')
    results = []
    for card in flightCards:
        departureLocation = card.find_element(By.CSS_SELECTOR, '.departure-loc').text
        departureTime = card.find_element(By.CSS_SELECTOR, '.departure-time').text
        arrivalLocation = card.find_element(By.CSS_SELECTOR, '.arrival-loc').text
        arrivalTime = card.find_element(By.CSS_SELECTOR, '.arrival-time').text

        # Find all price elements within the card
        prices = card.find_elements(By.CSS_SELECTOR, '.cheapest-cash-price.collapsed.ng-star-inserted')

        # Check if the prices list has the expected number of elements (2 in this case)
        if len(prices) == 2:
            economyPrice = prices[0].text if prices[0] else "Sold out"
            businessPrice = prices[1].text if prices[1] else "Sold out"
        else:
            # If there are not enough price elements, mark them as sold out
            economyPrice = "Sold out"
            businessPrice = "Sold out"

        flight_details = {
            'origin_airport': departureLocation,
            'arrival_airport': arrivalLocation,
            'departure_time': departureTime,
            'arrival_time': arrivalTime,
            'economy_price': economyPrice,
            'business_price': businessPrice
        }
        results.append(flight_details)

    print(results)
    driver.quit()
    return results


def rexScrape(functionality, flight_type):
    options = Options()
    options.add_argument("start-maximized")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)
    # options.add_argument("--headless")  # Runs Chrome in headless mode.

    # pathMac = '/Users/daniel/Downloads/chromedriver-mac-x64/chromedriver'
    # pathWindows = 'C:\\Users\\NZXT\\chromedriver-win64\\chromedriver.exe'
    # Change based on system path to chromedriver.exe

    # Macbook directory
    s = Service('C:\\Users\\NZXT\\chromedriver-win64\\chromedriver.exe')

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

    url = 'https://www.rex.com.au/'
    driver.get(url)

    originAirportDropdown = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, 'ContentPlaceHolder1_BookingHomepage1_OriginAirport')))
    originAirportDropdown.click()

    airport_code_mapping = {
        'depSydney': 'SYD',
        'depMelbourneTullamarine': 'MEL',
        'arrSydney': 'SYD',
        'arrMelbourneTullamarine': 'MEL'
        # Add more mappings as needed
    }

    if 'departureAirport' in functionality:
        departureAirportKey = functionality['departureAirport']
        departureAirportValue = airport_code_mapping[departureAirportKey]
        print(f'Departure Airport: {departureAirportKey} and Arrival Mapping: {departureAirportValue}')
        # Departure Airport: depSydney and Mapping: SYD
        sleep(2)
        departureAirportSelection = driver.find_element(By.CSS_SELECTOR, f'option[value="{departureAirportValue}"]')
        departureAirportSelection.click()
        print(f"Clicked {departureAirportValue}")

    destinationAirportDropdown = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, 'ContentPlaceHolder1_BookingHomepage1_DestinationAirport')))
    destinationAirportDropdown.click()

    if 'arrivalAirport' in functionality:
        arrivalAirportKey = functionality['arrivalAirport']
        arrivalAirportValue = airport_code_mapping[arrivalAirportKey]
        print(f'Arrival Airport: {arrivalAirportKey} and Arrival Mapping: {arrivalAirportValue}')
        sleep(2)

        print(f'Clicked {arrivalAirportValue}')
        selectElement = driver.find_element(By.ID, 'ContentPlaceHolder1_BookingHomepage1_DestinationAirport')
        for option in selectElement.find_elements(By.TAG_NAME, 'option'):
            if option.get_attribute('value') == "SYD":
                print("Found Sydney: ", option.text)
                driver.execute_script("arguments[0].scrollIntoView(true);", option)
                option.click()
                driver.execute_script("arguments[0].click();", option)
                break

            elif option.get_attribute('value') == 'MEL':
                print("Found Melbourne: ", option.text)
                driver.execute_script("arguments[0].scrollIntoView(true);", option)
                option.click()
                driver.execute_script("arguments[0].click();", option)
                break

    if flight_type == 'one-way':
        sleep(2)
        oneWayRadio = driver.find_element(By.CSS_SELECTOR, '.homebookingform-font-size')
        oneWayRadio.click()
        sleep(2)
        DateCalendar1 = driver.find_element(By.CSS_SELECTOR, '.datepick-input')
        DateCalendar1.click()

    departure_date_obj = datetime.strptime(functionality['departureDate'], '%Y-%m-%d')
    formatted_date = departure_date_obj.strftime('%b %Y')  # '%b' for abbreviated month name, '%Y' for full year

    print(formatted_date)

    monthFound = False

    while monthFound == False:
        findRexMonthYear = driver.find_elements(By.CSS_SELECTOR, '.month.drp-calendar-header')
        leftMMYY = findRexMonthYear[0]
        nextMonthSelector = driver.find_element(By.CSS_SELECTOR, '.next.available')
        try:
            if formatted_date == leftMMYY.text:
                monthFound = True
                print("Correct Month Found")

            else:
                nextMonthSelector.click()
                print(f'User input date: {formatted_date}, Left MMYY: {leftMMYY.text}')

        except StaleElementReferenceException:
            # If caught, this will go back to the start of the while loop and try to find the elements again
            # Search only goes till February 2025, if user input is past this, then this will be triggered
            #  Need better handling of this, such as blocking the option to choose date past February 2025
            continue

    # Your previous setup code, ensure the driver is initialized and pointed to the correct page

    formatted_numerical_date = departure_date_obj.strftime('%d').lstrip('0')  # Removes leading zero if present
    print(formatted_numerical_date)
    # First, locate the specific tbody by its XPath

    # Then, find all the tr elements within that tbody
    table_data = driver.find_elements(By.TAG_NAME, 'td')
    dateFound = False

    while not dateFound:
        for td in table_data:
            # Check if the td text matches the date and does not have 'off ends' in the class attribute
            if td.text.strip() == formatted_numerical_date and 'off ends' not in td.get_attribute('class'):
                print(f'Date found: {td.text}')
                td.click()
                dateFound = True
                break
            else:
                print(f'Incorrect date, going next. ({td.text})')

    bookNowButton = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, '.BookNowbtn')))
    bookNowButton.click()

    # sitekey = '6LfNWukUAAAAAAGvs5JOmzYUR-xSDIJH_Vi7z35I',
    # url = 'https://ibe2.rex.com.au/AvailFlight'
    api_key = 'c4d24eaca65b2982a0710f09c28d8dbe'

    solver = TwoCaptcha(api_key)

    try:
        result = solver.recaptcha(
            sitekey='6LfNWukUAAAAAAGvs5JOmzYUR-xSDIJH_Vi7z35I',
            url='https://ibe2.rex.com.au/AvailFlight'
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

        driver.execute_script(f"""
        $('#txtcaptcha').val("{result['code']}");
        $('.availCont').removeAttr('disabled');
        """)
        print("Complete")

        recaptchaSubmitButton = driver.find_element(By.CSS_SELECTOR, '.btn.btn-primary.d-block.btn-wait.availCont')
        recaptchaSubmitButton.click()

        print("Debug 11")
        # Switch back to the main content
        driver.switch_to.default_content()
        print("Back to default frame complete")

        sleep(5)

    except Exception as e:
        print('Failed to solve CAPTCHA:', e)


    WebDriverWait(driver, 20).until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR, '.f-strip'))
    )
    print("Debug 1")
    flightCards = driver.find_elements(By.CSS_SELECTOR, '.f-strip')
    results = []

    for element in flightCards:
        departsElements = element.find_element(By.CSS_SELECTOR, '.departs')
        arrivesElements = element.find_element(By.CSS_SELECTOR, '.arrives')

        departTime = departsElements.find_element(By.CSS_SELECTOR, '.time').text
        departAirport = departsElements.find_element(By.CSS_SELECTOR, '.port').text

        arrivalTime = arrivesElements.find_element(By.CSS_SELECTOR, '.time').text
        arrivalAirport = arrivesElements.find_element(By.CSS_SELECTOR, '.port').text

        try:
            flyEconomyElement = element.find_element(By.CSS_SELECTOR, '.fly.econ')
            econ_currency = flyEconomyElement.find_element(By.CSS_SELECTOR, '.currency')
            econ_dollar = flyEconomyElement.find_element(By.CSS_SELECTOR, '.dollar')
            econ_decimal = flyEconomyElement.find_element(By.CSS_SELECTOR, '.decimal')

            complete_priceEconomy = econ_currency.text + econ_dollar.text + econ_decimal.text
        except NoSuchElementException:
            complete_priceEconomy = "Sold Out"


        try:
            flyBusinessElement = element.find_element(By.CSS_SELECTOR, '.fly.biz')
            bus_currency = flyBusinessElement.find_element(By.CSS_SELECTOR, '.currency')
            bus_dollar = flyBusinessElement.find_element(By.CSS_SELECTOR, '.dollar')
            bus_decimal = flyBusinessElement.find_element(By.CSS_SELECTOR, '.decimal')

            complete_priceBusiness = bus_currency.text + bus_dollar.text + bus_decimal.text
        except NoSuchElementException:
            complete_priceBusiness = "Sold Out"


        flight_details = {
            'origin_airport': departAirport,
            'arrival_airport': arrivalAirport,
            'departure_time': departTime,
            'arrival_time': arrivalTime,
            'economy_price': complete_priceEconomy,
            'business_price': complete_priceBusiness
        }
        results.append(flight_details)



    print(results)
    driver.quit()
    return results


def virginScrape(functionality, flight_type):
    options = uc.ChromeOptions()
    options.add_argument('--blink-settings=imagesEnabled=false')  # Example option

    driver = uc.Chrome(options=options)
    # driver.delete_all_cookies() - Use if accidentally started in --headless mode and Virgin detected
    url = 'https://www.virginaustralia.com/au/en//'
    driver.get(url)
    origin_airport_dropdown = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR,
                                    '.fsTextInput.src-app-FlightSearchApp-components-TextInput-TextInput-module__fsTextInput--hr6I2')))
    sleep(2)
    origin_airport_dropdown.click()
    sleep(2)
    print("Print test 1")

    airport_code_mapping = {
        'depSydney': 'SYD',
        'depMelbourneTullamarine': 'MEL',
        'arrSydney': 'SYD',
        'arrMelbourneTullamarine': 'MEL'
        # Add more mappings as needed
    }

    def click_with_retry(driver, selector, retries=5, delay=5):
        """Attempts to click an element, with retries and a delay between attempts."""
        for attempt in range(retries):
            try:
                # Wait for the element to be clickable
                element = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, selector)))
                # Try clicking the element
                element.click()
                print("Click successful")
                return
            except ElementClickInterceptedException:
                print(f"Click intercepted, attempt {attempt + 1} of {retries}")
                if attempt > 0:
                    time.sleep(delay)
        raise Exception("Failed to click the element after several retries")


    if functionality['departureAirport']:
        origin_departure_key = (functionality['departureAirport'])
        origin_departure_value = airport_code_mapping[origin_departure_key]
        print(origin_departure_key, origin_departure_value)
        try:
            origin_airport_clicked_textarea = driver.find_element(By.CSS_SELECTOR, '.fsTextInputInput.vaThemeText.gb_unmask.src-app-FlightSearchApp-components-TextInput-TextInput-module__fsTextInputInput--e0oZm')

        except NoSuchElementException:
            sleep(2)
            print("Triggered timeout exception for DEPARTURE AIRPORT")
            origin_airport_dropdown.click()
            sleep(2)
            origin_airport_clicked_textarea = driver.find_element(By.CSS_SELECTOR, '.fsTextInputInput.vaThemeText.gb_unmask.src-app-FlightSearchApp-components-TextInput-TextInput-module__fsTextInputInput--e0oZm')

        # origin_airport_clicked_textarea = WebDriverWait(driver, 10).until(
            # EC.presence_of_element_located((By.CSS_SELECTOR,
                                           #  '.fsTextInputInput.vaThemeText.gb_unmask.src-app-FlightSearchApp-components-TextInput-TextInput-module__fsTextInputInput--e0oZm'))
        # )
        origin_airport_clicked_textarea.send_keys(origin_departure_value)


        try:
            origin_airport_dropdown_option = WebDriverWait(driver, 15).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR,
                                            '.fsSearchOptionItemButton.src-app-FlightSearchApp-components-TextInput-TextInput-module__fsSearchOptionItemButton--BgRYA')))
        except TimeoutException:
            print("Debug Statement 1.0")
            sleep(2)
            origin_airport_dropdown_option = WebDriverWait(driver, 15).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR,
                                            '.fsSearchOptionItemButton.src-app-FlightSearchApp-components-TextInput-TextInput-module__fsSearchOptionItemButton--BgRYA')))


        origin_airport_dropdown_option.click()


    if functionality['arrivalAirport']:
        arrival_airport_key = (functionality['arrivalAirport'])
        arrival_airport_value = airport_code_mapping[arrival_airport_key]
        print(arrival_airport_key, arrival_airport_value)

        airport_dropdown_finder = driver.find_elements(By.CSS_SELECTOR, '.fsTextInputInput.vaThemeText.gb_unmask.src-app-FlightSearchApp-components-TextInput-TextInput-module__fsTextInputInput--e0oZm')
        arrival_airport_dropdown = airport_dropdown_finder[1]
        # CSS is the same for origin and departure airport, so we need to find both elements as associate the index[1]
        # to be for arrival, therefore [0] would be origin
        arrival_airport_dropdown.send_keys(arrival_airport_value)
        try:
            arrival_airport_dropdown_option = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR,
                                            '.fsSearchOptionItemButton.src-app-FlightSearchApp-components-TextInput-TextInput-module__fsSearchOptionItemButton--BgRYA')))
        except TimeoutException:
            sleep(2)
            print("Triggered timeout exception for ARRIVAL AIRPORT")
            arrival_airport_dropdown.send_keys(arrival_airport_value)
            sleep(2)
            arrival_airport_dropdown_option = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR,
                                            '.fsSearchOptionItemButton.src-app-FlightSearchApp-components-TextInput-TextInput-module__fsSearchOptionItemButton--BgRYA')))


        arrival_airport_dropdown_option.click()

    nextButton_to_date_selection = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR,
                                    '.vaButton.vaThemeButton.vaTracked.src-app-FlightSearchApp-modals-screens-FromToScreen-FromToScreen-module__fsFromToScreenFooterNextButton--VhkoZ.vaButtonPrimary')))
    nextButton_to_date_selection.click()



    if flight_type == 'one-way':
        one_way_button = '.src-app-FlightSearchApp-components-TripSelection-TripSelection__tripSelectionBtn--wlqrl.src-app-FlightSearchApp-components-TripSelection-TripSelection__oneway--d8yhv'
        try:
            click_with_retry(driver, one_way_button)
        except Exception as e:
            print(e)
            print("OneWay Click Failed")
        driver.find_element(By.CSS_SELECTOR, one_way_button).click()

    monthFound = False
    departure_date_obj = datetime.strptime(functionality['departureDate'], '%Y-%m-%d')
    formatted_date = departure_date_obj.strftime('%B %Y')

    while not monthFound:
        leftMMYY = driver.find_element(By.CSS_SELECTOR,
                                       '.react-calendar__navigation__label__labelText.react-calendar__navigation__label__labelText--from')
        if leftMMYY.text == formatted_date:
            print(f'MATCH: Left MMYY: {leftMMYY.text}, Formatted Date: {formatted_date}')
            monthFound = True
            break
        else:
            print(f'NO MATCH: Left MMYY: {leftMMYY.text}, Formatted Date: {formatted_date}')
            nextMonthButton = driver.find_element(By.CSS_SELECTOR,
                                                  '.react-calendar__navigation__arrow.react-calendar__navigation__next-button')
            nextMonthButton.click()

    abbr_finder = driver.find_elements(By.TAG_NAME, 'abbr')
    departure_date_obj = datetime.strptime(functionality['departureDate'], '%Y-%m-%d')
    singular_day_value = departure_date_obj.strftime('%d').lstrip('0')

    dateFound = False
    print(f"Target Date: {singular_day_value}")

    while not dateFound:
        for abbr in abbr_finder:
            if abbr.text == singular_day_value:
                print(f'{abbr.text} is a match to {singular_day_value}')
                abbr.click()
                dateFound = True
                break
            else:
                print(f'{abbr.text} is NOT a match to {singular_day_value}')

    try:
        after_date_selection_next_button = WebDriverWait(driver, 15).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR,
                                    '.vaButton.vaThemeButton.vaTracked.src-app-FlightSearchApp-modals-screens-DatesScreen-DatesScreen-module__fsDatesScreenFooterNextButton--jfhBw.vaButtonPrimary')))
    except TimeoutException:
        sleep(2)
        after_date_selection_next_button = WebDriverWait(driver, 15).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR,
                                    '.vaButton.vaThemeButton.vaTracked.src-app-FlightSearchApp-modals-screens-DatesScreen-DatesScreen-module__fsDatesScreenFooterNextButton--jfhBw.vaButtonPrimary')))

    after_date_selection_next_button.click()
    print("Clicked Next Button (Second Last)")

    final_lets_fly_button = WebDriverWait(driver, 30).until(
        EC.element_to_be_clickable(driver.find_element(By.CSS_SELECTOR,
                                                       '.vaButton.vaThemeButton.vaTracked.src-app-FlightSearchApp-modals-screens-GuestsScreen-GuestsScreen-module__fsGuestsScreenFooterNextButton--mOaeJ.vaButtonPrimary'))
    )

    try:
        final_lets_fly_button.click()  # Attempt to click the button
    except WebDriverException as e:
        print(f"WebDriverException encountered: {e}")  # Print the exception message
        print("Trying to continue...")
        # Optionally, try to recover or retry the action here
        time.sleep(5)  # Wait for a bit before trying again (if that makes sense in your context)
        try:
            # Attempt the click again or do something else to try to recover
            final_lets_fly_button.click()
        except WebDriverException as e:
            # If it fails again, decide what to do next:
            # You can continue, return, or raise the exception again
            print(f"Retry also failed: {e}")


    print("Clicked Lets Fly Button (Last)")


    WebDriverWait(driver, 30).until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR, '.itinerary-part-offer-header'))
    )
    flight_cards_mini_summary = driver.find_elements(By.CSS_SELECTOR, '.itinerary-part-offer-header')
    results = []
    for flight_card in flight_cards_mini_summary:
        # Find the span with class 'code' within the flight_card element
        airport_codes = flight_card.find_elements(By.CSS_SELECTOR, '.code')
        if len(airport_codes) >= 2:
            origin_airport_virgin_card = airport_codes[0].text
            arrival_airport_virgin_card = airport_codes[1].text

            # Use flight_card.find_element to find elements specific to this flight card
            airport_originTime = flight_card.find_element(By.CSS_SELECTOR,
                                                          '.ducp-component-flight-times.time.originTime').text
            airport_arrivalTime = flight_card.find_element(By.CSS_SELECTOR,
                                                           '.ducp-component-flight-times.time.destinationTime').text

            # Initialize prices as "Available" (or some default value) before trying to find them
            complete_priceEconomy = "Available"
            complete_priceBusiness = "Available"

            try:
                economyPricing = flight_card.find_element(By.CSS_SELECTOR, '.cabin-offer.economy')
                currencyEcon = economyPricing.find_element(By.CSS_SELECTOR, "span.currency.symbol")
                priceNumberEcon = economyPricing.find_element(By.CSS_SELECTOR, '.number')
                complete_priceEconomy = currencyEcon.text + priceNumberEcon.text
            except NoSuchElementException:
                complete_priceEconomy = "Sold out"

            try:
                businessPricing = flight_card.find_element(By.CSS_SELECTOR, '.cabin-offer.business')
                currencyBus = businessPricing.find_element(By.CSS_SELECTOR, "span.currency.symbol")
                priceNumberBus = businessPricing.find_element(By.CSS_SELECTOR, '.number')
                complete_priceBusiness = currencyBus.text + priceNumberBus.text
            except NoSuchElementException:
                complete_priceBusiness = "Sold out"

            print(f'Economy: {complete_priceEconomy} - Business: {complete_priceBusiness}')

            flight_details = {
                    'origin_airport': origin_airport_virgin_card,
                    'arrival_airport': arrival_airport_virgin_card,
                    'departure_time': airport_originTime,
                    'arrival_time': airport_arrivalTime,
                    'economy_price': complete_priceEconomy,
                    'business_price': complete_priceBusiness
            }
        # Append the dictionary to the results list
            results.append(flight_details)

    print(results)
    driver.quit()
    return results


if __name__ == "__main__":
    print("Hello World")
