from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as EC
import time
import re

def element_exists(driver, locator, timeout=2):
    try:
        WebDriverWait(driver, timeout).until(EC.presence_of_element_located(locator))
        return True
    except TimeoutException:
        return False

def wait_for_element_stability(driver, locator, timeout=30):
    WebDriverWait(driver, timeout).until(
        EC.presence_of_element_located(locator)
    )
    previous_value = None
    for _ in range(timeout):
        element = driver.find_element(*locator)
        current_value = element.get_attribute('outerHTML')
        if current_value == previous_value:
            break
        previous_value = current_value
        time.sleep(1)
    else:
        raise TimeoutException("Element did not stabilize within the timeout period")


def extract_dates(text):
    # Regular expression to find dates in the format MM/DD/YY
    date_pattern = r'(\d{1,2}/\d{1,2}/\d{2})'

    # Find all occurrences of the date pattern
    dates = re.findall(date_pattern, text)
    
    if len(dates) >= 2:
        start_date = dates[0]
        end_date = dates[1]
        return start_date, end_date
    else:
        return None, None

def getProductNumber(driver):
    try:
        itemNumber = driver.find_element(By.CSS_SELECTOR, 'div.item-number > span').text
        return itemNumber
    except Exception as e:
        #print(f"Error occurred: {e}")
        pass

    try:
        itemNumber = driver.find_element(By.CSS_SELECTOR, 'div.item-number').text.strip().split()[1]
        return itemNumber
    except Exception as e:
        #print(f"Error occurred: {e}")
        pass
    return -1

def getProductPrice(driver):
    try:
        stickerPrice = driver.find_element(By.CSS_SELECTOR, 'span.op-value').text
        if stickerPrice:
            return stickerPrice
        else:
            stickerPrice = driver.find_element(By.CSS_SELECTOR, 'span.value').text
            return stickerPrice
    except:
        print("Price not found")

def getProductPromotion(driver):
    try:
        discount = driver.find_element(By.CSS_SELECTOR, 'p.merchandisingText').text
        promotionText = driver.find_element(By.CSS_SELECTOR, 'p.PromotionalText').text
        startDate, endDate = extract_dates(promotionText)
        return {
            "price": discount,
            "startDate": startDate,
            "endDate": endDate
        }
    except Exception as e:
        print("Deal not found")

def getProductDetails(driver):
    try:
        if element_exists(driver, (By.CSS_SELECTOR, 'span.value'), 2):
            wait_for_element_stability(driver, (By.CSS_SELECTOR, 'span.value'), 4)
            itemNumber = getProductNumber(driver)
            stickerPrice = getProductPrice(driver)
            promotion = getProductPromotion(driver)
            print(itemNumber)
            print(stickerPrice)
            print(promotion)
    except Exception as e:
        print(f"Error occurred: {e}")
        pass

def getProductsFromItemNumbers(item_numbers):
    service = Service("chromedriver.exe")
    driver = webdriver.Chrome(service=service)
    for item_number in item_numbers:
        driver.get("https://www.costco.com/s?dept=All&keyword=" + item_number)
        getProductDetails(driver)
    driver.quit()

def getProductFromItemNumber(item_number):
    service = Service("chromedriver.exe")
    driver = webdriver.Chrome(service=service)
    driver.get("https://www.costco.com/s?dept=All&keyword="+item_number)
    getProductDetails(driver)
    driver.quit()




# service = Service("chromedriver.exe")
# driver = webdriver.Chrome(service=service)
# driver.get("https://www.costco.com/CatalogSearch?keyword=OFF&dept=All&sortBy=item_startDate+desc")

# # Loop through each product element
# while True:
#     # Find all elements with class containing 'product'
#     time.sleep(10)
#     product_elements = driver.find_elements(By.CSS_SELECTOR, '#productList > div > div > a')
#     for product in product_elements:
#         try:
#             # Get the URL from the href attribute
#             product_url = product.get_attribute('href')
#             if ".product." in product_url:
#                 print(f"Product URL: {product_url}")
#                 # Switch to the new tab
#                 driver.execute_script("window.open(arguments[0]);", product_url)
#                 driver.switch_to.window(driver.window_handles[-1])

#                 getProductDetails(driver)

#         except Exception as e:
#             print(f"Error occurred: {e}")
#         finally:
#             driver.close()
#             driver.switch_to.window(driver.window_handles[0])
    
#     next_page_button = driver.find_element(By.CSS_SELECTOR, "button[aria-label='Go to next page']")
#     if next_page_button:
#         next_page_button.click()
#     else:
#         break

# # Close the WebDriver
# driver.quit()