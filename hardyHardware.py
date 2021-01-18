import sqlite3
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from locator import *

#function for printing all the items
def get_items():
    with conn:
        db.execute("SELECT * FROM Items")
        rows = db.fetchall()
        i = 1
        for row in rows:
            name, stars, price, description, overeview = row
            print(f"Item {i}- Name: {name}")
            print(f"        Stars: {stars}")
            print(f"        Price: {price}")
            print(f"        Description: {description}")
            print(f"        Overeview: {overeview}")

            i += 1

conn = sqlite3.connect('hardyDB.db')
db = conn.cursor()

#first table creation
#db.execute(""" CREATE TABLE Items (
#            Name text,
#            Stars text,
#            price text,
#            Description text,
#            Overeview text
#            )""")

#clear the database table
db.execute("DELETE FROM Items")

#open webdriver
driver = webdriver.Chrome(executable_path="chromedriver.exe")
driver.get("http://class.kofax.com/hardyhardware/")
driver.find_element(*MainLocators.PRODUCTS_LISTING_BUTTON).click()
#wait until the page has loaded
try:
    exwait = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located(MainLocators.PRODUCTS_LISTING_BREADCRUMB))
    #loop the first 3 pages
    for i in range(1,4):
        ##loop through all of the products in the page
        for x in range (0,20):
            #I have to re-initialize the elements every loop run because every time I go back to the product's page the DOM changes.
            elements = driver.find_elements(*MainLocators.ALL_PRODUCTS)
            element = elements[x]
            #click the product's name to enter its page
            element.find_element(*MainLocators.PRODUCT_NAME).click()
            #wait until the page has loaded
            exwait = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located(ProductPageLocators.MAIN_IMAGE))
            #start pulling information
            name = driver.find_element(*ProductPageLocators.NAME).text
            stars = driver.find_element(*ProductPageLocators.STARS).get_attribute("value")
            stars += " stars"
            desc = driver.find_element(*ProductPageLocators.DESCRIPTION).find_element_by_tag_name("p").text
            over = driver.find_element(*ProductPageLocators.OVEREVIEW).find_element_by_tag_name("p").text
            price = driver.find_element(*ProductPageLocators.PRICE).text
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
            exwait = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located(MainLocators.PRODUCTS_LISTING_BREADCRUMB))

        #we finished a page, go to the next page
        driver.find_element_by_xpath(f'//*[@id="hikashop_category_information_module_88"]/div/form/div/div/ul/a[{i}]').click()
        #check that the page has loaded
        exwait = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'hikashop_products_listing')))

finally:
    driver.quit()

get_items()





conn.commit()
conn.close()