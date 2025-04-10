import json
import time

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

options = Options()
options.add_argument("--headless")

driver = webdriver.Chrome()
driver.get('https://www.axcapital.ae/rent/dubai/properties-for-rent')
time.sleep(3)
cards = driver.find_elements(By.CSS_SELECTOR, ".property-card")

extracted_data = []

for card in cards:
    try:
        title_el = card.find_element(By.CSS_SELECTOR, 'strong.mb-4.block.flex-grow.text-2xl.text-white')
        title = title_el.text

        location_el = card.find_element(By.CSS_SELECTOR, 'p.mb-1.flex.items-center.text-white')
        location = location_el.text

        price_el = card.find_element(By.XPATH,
                        ".//div[contains(@class, 'flex justify-between') and contains(@class, 'border-t-[1px]')]//span")
        price = price_el.text

        img_el = card.find_element(By.CSS_SELECTOR, 'img.swiper-lazy')
        img_url = img_el.get_attribute("src")

        pr_type_el = card.find_element(By.CSS_SELECTOR, 'span.capitalize')
        property_type = pr_type_el.text

        property_info ={
            'title': title,
            'location': location,
            'price': price,
            'property type': property_type,
            'image url': img_url
        }
        extracted_data.append(property_info)

    except Exception as e:
        print("error extracting the data: ", e)


json_data = json.dumps(extracted_data, indent=2)
with open("axData.json", "w") as f:
    f.write(json_data)


print(driver.title)
driver.quit()