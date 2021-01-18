from selenium.webdriver.common.by import By

class MainLocators(object):
    PRODUCTS_LISTING_BUTTON = (By.LINK_TEXT, "Products listing")
    PRODUCTS_LISTING_BREADCRUMB = (By.XPATH, '//*[@id="jsn-pos-breadcrumbs"]/ul/li[3]/span[2]')
    ALL_PRODUCTS = (By.CLASS_NAME, "hikashop_container")
    PRODUCT_NAME = (By.CLASS_NAME, "hikashop_product_name")

class ProductPageLocators(object):
    MAIN_IMAGE = (By.ID, "hikashop_main_image")
    NAME = (By.ID, "hikashop_product_name_main")
    STARS = (By.NAME, "hikashop_vote_rating")
    DESCRIPTION = (By.CLASS_NAME, "Description")
    OVEREVIEW = (By.XPATH, '//*[@id="hikashop_product_description_main"]/div[2]')
    PRICE = (By.XPATH, '//*[@id="hikashop_product_price_main"]/span[1]/span[2]')