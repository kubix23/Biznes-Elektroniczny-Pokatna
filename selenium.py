import random

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class Tester:
    def __init__(self, url):
        self.url = url
        self.driver = webdriver.Chrome()
        self.driver.get(self.url)
    def add_to_cart_test(self, cat):
        collapse_menu = self.driver.find_element(by=By.CLASS_NAME, value="top-menu")
        action = ActionChains(driver=self.driver)
        action.move_to_element(collapse_menu).perform()
        cat1 = self.driver.find_element(by=By.LINK_TEXT, value=cat)
        action.move_to_element(cat1).click().perform()

        for i in range(5):
            products = self.driver.find_elements(by=By.CLASS_NAME, value="product-title")
            products[i].click()
            additional_product_amount = random.randint(0,4)
            for j in range(additional_product_amount):
                self.driver.find_element(by=By.CLASS_NAME, value="touchspin-up").click()
            self.driver.find_element(by=By.CLASS_NAME, value="add-to-cart").click()
            self.driver.back()


if __name__ == "__main__":
    host = 'http://localhost:8080/index.php'
    tester = Tester(host)
    tester.add_to_cart_test("Karty graficzne AMD")
    tester.add_to_cart_test("Płyty główne Socket AM4")
    tester.driver.quit()
