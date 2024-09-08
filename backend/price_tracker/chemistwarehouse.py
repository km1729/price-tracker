from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from urllib.parse import urlparse
from bs4 import BeautifulSoup
import time

# Set up Selenium WebDriver with options
options = Options()
options.add_argument("--headless")  # Optional: Run in headless mode
options.add_argument("--no-sandbox")  # Required for some systems
options.add_argument("--disable-dev-shm-usage")  # Overcome limited resource problems

# Initialize the Service for ChromeDriver
service = Service('/usr/bin/chromedriver')

# Initialize the Chrome WebDriver using the Service
driver = webdriver.Chrome(service=service, options=options)

def get_soup_with_selenium(url):
    driver.get(url)
    time.sleep(3)  # Give the page time to load
    page_source = driver.page_source
    return BeautifulSoup(page_source, 'html.parser')

def get_brand(soup):
    breadcrumbs = soup.find("ul", {"class": "breadcrumbs"})
    if breadcrumbs:
        brand = breadcrumbs.find_all("a")[-1].text.strip()  # Get the last <a> tag's text
        return brand
    return None

def get_product_name(soup):
    product_details_td = soup.find("td", {"class": "product_details"})
    if product_details_td:
        product_name_div = product_details_td.find("div", {"class": "product-name"})
        if product_name_div:
            product_name_tag = product_name_div.find("h1")
            if product_name_tag:
                return product_name_tag.text.strip()
    return "Product name not found"

def get_product_id(soup):
    product_details_td = soup.find("td", {"class": "product_details"})
    
    if product_details_td:
        product_id_div = product_details_td.find("div", {"class": "product-id"})
        if product_id_div:
            product_id_text = product_id_div.text.strip()
            # Extract the numeric part after "Product ID: "
            product_id = product_id_text.replace("Product ID: ", "")
            return product_id
        else:
            return "Product ID not found"
    else:
        return "TD with class 'product_details' not found"

def get_price(soup):
    product_details_td = soup.find("td", {"class": "product_details"})
    if product_details_td:
        price_div = product_details_td.find("div", {"class": "Price"})
        if price_div:
            price_span = price_div.find("span", {"class": "product__price"})
            if price_span:
                price_str = price_span.text.strip()
                return float(price_str.replace('$',''))
    return "Price not found"

def get_supplier(url):
    parsed_url = urlparse(url)
    supplier = parsed_url.netloc.split('.')[1]  # Extracts the second part, e.g., 'chemistwarehouse'
    return supplier

def extract(url: str):
    soup = get_soup_with_selenium(url)
    company = get_brand(soup)
    product_name = get_product_name(soup)
    price = get_price(soup)
    product_id = get_product_id(soup)
    supplier = get_supplier(url)
    return company, product_name, price, product_id, supplier

if __name__ == '__main__':
    url = 'https://www.chemistwarehouse.com.au/buy/135282/blackmores-bio-c-1000-180-tablets-exclusive-size'
    company, product_name, price, product_id, supplier = extract(url)
    print(company, product_name, price, product_id, supplier)
