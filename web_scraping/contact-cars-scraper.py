from seleniumbase import Driver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
import pandas as pd
import time


def initialize_driver():
    """Initialize the WebDriver"""
    driver = Driver(uc=True)
    return driver


def fetch_page(url, driver):
    """Fetch the URL"""
    driver.get(url)


def scrape_page_source(driver):
    """Get the page source"""
    return driver.page_source


def get_titles(driver):
    """Find all titles by CSS selector"""
    return driver.find_elements(By.CSS_SELECTOR, "h2.sub-h-lg.text-brand-900.truncate")


def get_locations(driver):
    """Find all parent div elements by CSS selector"""
    return driver.find_elements(
        By.CSS_SELECTOR, "div.flex.items-center.txt-sm.text-dark-blue"
    )


def get_car_listings(driver):
    """Find all parent div elements by CSS selector"""
    return driver.find_elements(
        By.CSS_SELECTOR, "div.flex.flex-wrap.content-start.gap-2.p-3.pt-0.bg-white-900"
    )


def get_prices(driver):
    """Find all prices by CSS selector"""
    return driver.find_elements(By.CSS_SELECTOR, "span.sub-h-lg.me-1")


def get_min_down_payments(driver):
    """Find all parent div elements by CSS selector"""
    return driver.find_elements(
        By.CSS_SELECTOR,
        "div.flex.items-center.justify-between.text-orange-500.flex-wrap",
    )


def get_links(driver):
    """Find all links by CSS selector"""
    return driver.find_elements(
        By.CSS_SELECTOR, "a.p-3.pt-0.bg-white-900.flex.flex-col.justify-between.h-20"
    )


def scrape_data_from_titles(titles):
    """Iterate through each title and extract text"""
    title_list = []
    for title in titles:
        title_text = title.text
        title_list.append(title_text)
    return title_list


def scrape_data_from_locations(listings):
    """Iterate through each listing and extract location data"""
    governorate_list = []
    city_list = []
    for listing in listings:
        try:
            governorate = listing.find_element(
                By.CSS_SELECTOR, "a.hover\\:text-brand-600.hover\\:underline"
            ).text
            city = listing.find_elements(
                By.CSS_SELECTOR, "a.hover\\:text-brand-600.hover\\:underline"
            )[1].text
            governorate_list.append(governorate)
            city_list.append(city)
        except (NoSuchElementException, IndexError):
            governorate_list.append("not specified")
            city_list.append("not specified")
    return governorate_list, city_list


def scrape_data_from_car_listings(listings):
    """Iterate through each listing and extract car data"""
    maker_list = []
    model_list = []
    model_year_list = []
    mileage_list = []
    car_type_list = []
    for listing in listings:
        try:
            children = listing.find_elements(By.CSS_SELECTOR, "span.txt-2xs.me-1")
            maker_list.append(children[0].text)
            model_list.append(children[1].text)
            model_year_list.append(children[2].text)
            mileage_list.append(children[3].text)
            car_type_list.append(children[4].text)
        except (NoSuchElementException, IndexError):
            maker_list.append("not specified")
            model_list.append("not specified")
            model_year_list.append("not specified")
            mileage_list.append("not specified")
            car_type_list.append("not specified")
    return maker_list, model_list, model_year_list, mileage_list, car_type_list


def scrape_data_from_prices(prices):
    """Iterate through each price element and extract text"""
    price_list = []
    for price in prices:
        price_text = price.text
        price_list.append(price_text)
    return price_list


def scrape_data_from_min_down_payments(min_down_payments):
    """Iterate through each listing and extract minimum down payment data"""
    min_dp_list = []
    for listing in min_down_payments:
        try:
            children = listing.find_elements(By.CSS_SELECTOR, "span.txt-lg.mx-1")
            min_dp_list.append(children[0].text)
        except (NoSuchElementException, IndexError):
            min_dp_list.append("no minimum down payment specified")
    return min_dp_list


def scrape_data_from_links(link_element):
    """Iterate through each link element and extract href"""
    link_list = []
    for link in link_element:
        link = link.get_attribute("href")
        link_list.append(link)
    return link_list


# Base URL of the website
base_url = "https://contactcars.com/en/used-cars?page="  # Replace with your base URL

# Define the number of pages you want to scrape
num_pages = 109  # The maximum amount of pages as of April the 13th 2024, increase pages as needed

# Initialize the WebDriver
driver = initialize_driver()

title_list = []
governorate_list = []
city_list = []
maker_list = []
model_list = []
model_year_list = []
mileage_list = []
car_type_list = []
price_list = []
min_dp_list = []
link_list = []


# Iterate through the pages
for page_num in range(1, num_pages + 1):
    # Construct the URL for the current page
    url = f"{base_url}{page_num}"

    try:
        # Fetch the URL
        fetch_page(url, driver)

        # Get the page source
        page_source = scrape_page_source(driver)

        # Print the title of the page as a simple example
        print(f"Page {page_num} Title:", driver.title)

    except Exception as e:
        print(f"Error occurred while fetching page {page_num}: {e}")

    time.sleep(5)

    # Get titles data
    titles = get_titles(driver)
    title_list.extend(scrape_data_from_titles(titles))

    # Get locations data
    locations = get_locations(driver)
    governorate, city = scrape_data_from_locations(locations)
    governorate_list.extend(governorate)
    city_list.extend(city)

    # Get car listings data
    car_listings = get_car_listings(driver)
    maker, model, model_year, mileage, car_type = scrape_data_from_car_listings(
        car_listings
    )
    maker_list.extend(maker)
    model_list.extend(model)
    model_year_list.extend(model_year)
    mileage_list.extend(mileage)
    car_type_list.extend(car_type)

    # Get prices data
    prices = get_prices(driver)
    price_list.extend(scrape_data_from_prices(prices))

    # Get min down payments data
    min_down_payments = get_min_down_payments(driver)
    min_dp_list.extend(scrape_data_from_min_down_payments(min_down_payments))

    # Get links data
    link_element = get_links(driver)
    link_list.extend(scrape_data_from_links(link_element))


# Close the driver
driver.quit()

print("Title List:", len(title_list))
print("Maker List:", len(maker_list))
print("Model List:", len(model_list))
print("Model Year List:", len(model_year_list))
print("Mileage List:", len(mileage_list))
print("Car Type List:", len(car_type_list))
print("Price List:", len(price_list))
print("Minimum Down Payment List:", len(min_dp_list))
print("Link:", len(link_list))

# Turn the lists into a dictionary
data = {
    "Title": title_list,
    "Governorate": governorate_list,
    "City": city_list,
    "Maker": maker_list,
    "Model": model_list,
    "Model Year": model_year_list,
    "Mileage": mileage_list,
    "Car Type": car_type_list,
    "Price": price_list,
    "Minimum Down Payment": min_dp_list,
    "Link": link_list,
}

# Create a DataFrame from the dictionary
df = pd.DataFrame(data)

# Save the DataFrame to a CSV file
df.to_csv("raw_contactcars_data.csv", index=False)
