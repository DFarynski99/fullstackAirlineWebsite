from time import sleep, time
import pandas as pd
import requests as requests
from selenium import webdriver
from bs4 import BeautifulSoup
import os
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
import requests
import time

lst_prices = []
lst_airline = []
lst_departure = []


def notify_ifttt(price):
    event_name = 'price_drop'
    key = 'o68zKbvAHahsn_vcuM8O_PHpKoBIN_aCzS0e22_wHBd'  # Replace with your IFTTT Webhooks key
    url = f'https://maker.ifttt.com/trigger/price-drop/with/key/o68zKbvAHahsn_vcuM8O_PHpKoBIN_aCzS0e22_wHBd'

    # Data to pass to the email body, you can add more with Value2, Value3 etc.
    data = {'value1': lst_prices, 'value2': lst_airline, 'value3': lst_departure}
    requests.post(url, json=data)
    response = requests.post(url, json=data)
    print(f'Notification sent for price drop: {lst_prices}')


def check_prices_and_notify(lst_prices):
    for price_str in lst_prices:
        # Clean the price string and convert it to a float
        price_value = float(price_str.replace('$', ''))

        # Check if the price is below $200
        if price_value < 190:
            print(f"Price dropped to ${price_value}, sending notification...")
            notify_ifttt(f'$ {price_value}')
            print("")
        else:
            print(f"Price is ${price_value}, no notification sent.")
            print("")


def scraperLogic():
    driver = webdriver.Chrome()
    url = 'https://www.skyscanner.com.au/transport/flights/mel/syd/240225/?adultsv2=1&airlines=-32166,-31933,-31694&cabinclass=economy&childrenv2=&departure-times=1080-1439&duration=180&inboundaltsenabled=false&outboundaltsenabled=false&ref=home&rtn=0&stops=!oneStop,!twoPlusStops'

    driver.get(url)
    print("Waiting 25 seconds for all elements to load")
    sleep(25)  # Waits for the page to load. Consider using WebDriver wait conditions instead for better reliability.

    loadMoreButtonXPath = "//button[@class='BpkButton_bpk-button__YzJlY BpkButton_bpk-button--secondary__OGE0O']"

    try:
        # Try to find and click the "Load More" button
        driver.find_element(By.XPATH, loadMoreButtonXPath).click()
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


def clearVariables():
    lst_prices.clear()
    lst_airline.clear()
    lst_departure.clear()


def main():
    while True:  # This loop will run indefinitely
        scraperLogic()
        check_prices_and_notify(lst_prices)
        clearVariables()
        print("Sleeping for 900 seconds (15 minutes) before checking again...")
        time.sleep(900)  # Sleep after checking all prices, before starting over


if __name__ == "__main__":
    main()
