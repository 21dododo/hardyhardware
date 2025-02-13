import sqlite3
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from locator import *

WEBSITE_URL = "http://class.kofax.com/hardyhardware/"
NUM_OF_PAGES = 3

#function for printing all the items
def print_items(db):

    db.execute("SELECT * FROM Items")
    rows = db.fetchall()
    i = 1
    for row in rows:
        name, stars, price, description, overeview = row
        print(f"Item {i}- Name: {name}")
        print(f"        Stars: {stars}")
        print(f"        Price: ${price}")
        print(f"        Description: {description}")
        print(f"        Overeview: {overeview}")

        i += 1
def main():
    conn = sqlite3.connect('hardyDB.db')
    db = conn.cursor()

    #first table creation
    db.execute("DROP TABLE Items")
    db.execute(""" CREATE TABLE IF NOT EXISTS Items (
                Name text,
                Stars FLOAT,
                price FLOAT,
                Description text,
                Overeview text
                )""")

    #clear the database table
    db.execute("DELETE FROM Items")

    #open webdriver
    driver = webdriver.Chrome(executable_path="chromedriver.exe")
    driver.get(WEBSITE_URL)
    driver.find_element(*MainLocators.PRODUCTS_LISTING_BUTTON).click()
    #wait until the page has loaded
    try:
        WebDriverWait(driver, 10).until(
        EC.presence_of_element_located(MainLocators.PRODUCTS_LISTING_BREADCRUMB))
        #loop the first 3 pages
        for page in range(1, NUM_OF_PAGES + 1):
            if page != 1:
                # go to the next page unless it's our first iteration (we do page + 2 because the button of page 1 is in li[3] and so on)
                driver.find_element_by_xpath(f'//*[@id="hikashop_category_information_module_88"]/div/form/div/div/ul/li[{page + 2}]/a').click()
                # check that the page has loaded
                WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, 'hikashop_products_listing')))
            ##loop through all of the products in the page
            elements = driver.find_element(By.CLASS_NAME, "hikashop_products")
            num_of_elements = len (elements.find_elements (*MainLocators.ALL_PRODUCTS))
            for x in range (0, num_of_elements):
                #I have to re-initialize the elements every loop run because every time I go back to the product's page the DOM changes.
                elements = driver.find_elements(*MainLocators.ALL_PRODUCTS)
                element = elements[x]
                #click the product's name to enter its page
                element.find_element(*MainLocators.PRODUCT_NAME).click()
                #wait until the page has loaded
                WebDriverWait(driver, 10).until(
                EC.presence_of_element_located(ProductPageLocators.MAIN_IMAGE))
                #start pulling information
                name = driver.find_element(*ProductPageLocators.NAME).text
                stars = float (driver.find_element(*ProductPageLocators.STARS).get_attribute("value"))
                desc = driver.find_element(*ProductPageLocators.DESCRIPTION).find_element_by_tag_name("p").text
                over = driver.find_element(*ProductPageLocators.OVEREVIEW).find_element_by_tag_name("p").text
                price = driver.find_element(*ProductPageLocators.PRICE).text[1:]
                price = price.replace(',', '')
                price = float (price)
                #insert to database
                db.execute("INSERT INTO Items VALUES (?, ?, ?, ?, ?)", (name, stars, price, desc, over ))

                #go back to previous page
                driver.back()
                #sometimes the page "crashes" and we need to refresh, here we check if the page has loaded or does it need refreshing
                try:
                    driver.find_element_by_class_name('hikashop_products_listing')
                except NoSuchElementException:
                    driver.refresh()
                #wait until the page has loaded
                WebDriverWait(driver, 10).until(
                EC.presence_of_element_located(MainLocators.PRODUCTS_LISTING_BREADCRUMB))

    finally:
        driver.quit()

    print_items(db)

    conn.commit()
    conn.close()

if __name__ == "__main__":
    main()