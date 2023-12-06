import random

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys


class Tester:
    def __init__(self, url):
        self.url = url
        self.driver = webdriver.Chrome()
        self.driver.get(self.url)

    def remove_3_from_cart(self):
        self.driver.find_element(by=By.CLASS_NAME, value="shopping-cart").click()
        for _ in range(3):
            self.driver.find_element(by=By.CLASS_NAME, value="remove-from-cart").click()




    def search_test(self):
        search_box = self.driver.find_element(by=By.NAME, value="s")
        search_box.send_keys("rx 6700")
        search_box.send_keys(Keys.ENTER)

        products = self.driver.find_elements(by=By.CLASS_NAME, value="product-title")

        not_found = True
        while not_found:
            product = products[random.randint(0, len(products) - 1)]
            try:
                product.find_element(By.CLASS_NAME, value="out_of_stock")
            except:
                not_found = False
        product.click()
        self.driver.find_element(by=By.CLASS_NAME, value="add-to-cart").click()
        self.driver.back()
        self.driver.refresh()

    def add_to_cart_test(self, cat):
        collapse_menu = self.driver.find_element(by=By.CLASS_NAME, value="top-menu")
        action = ActionChains(driver=self.driver)
        action.move_to_element(collapse_menu).perform()
        cat1 = self.driver.find_element(by=By.LINK_TEXT, value=cat)
        action.move_to_element(cat1).click().perform()

        for i in range(5):
            products = self.driver.find_elements(by=By.CLASS_NAME, value="product-title")
            products[i].click()
            additional_product_amount = random.randint(0, 4)
            for j in range(additional_product_amount):
                self.driver.find_element(by=By.CLASS_NAME, value="touchspin-up").click()
            self.driver.find_element(by=By.CLASS_NAME, value="add-to-cart").click()
            self.driver.back()

    def register(self):
        self.driver.find_element(By.PARTIAL_LINK_TEXT, "Zaloguj").click()
        self.driver.find_element(By.PARTIAL_LINK_TEXT, "Nie masz").click()
        self.driver.find_element(By.CLASS_NAME, "custom-radio").click()
        self.driver.find_element(By.NAME, "firstname").send_keys("Dominus")
        self.driver.find_element(By.NAME, "lastname").send_keys("Faustinus")

        email_number = random.randint(0,99999999)
        self.driver.find_element(By.NAME, "email").send_keys("magos_dominus@omnissiah.mrs-" + str(email_number))
        self.driver.find_element(By.NAME, "password").send_keys("011000010110010001101101011010010110111000001010")
        self.driver.find_element(By.NAME, "birthday").send_keys("2018-11-15")

        checkboxes = self.driver.find_elements(By.CLASS_NAME, "custom-checkbox")
        for box in checkboxes:
            box.click()
        self.driver.find_element(By.CLASS_NAME, "form-control-submit").click()

    def order(self):
        self.driver.find_element(by=By.CLASS_NAME, value="shopping-cart").click()
        self.driver.find_element(by=By.CLASS_NAME, value="btn-primary").click()
        self.driver.find_element(By.NAME, "address1").send_keys("Nottingham NG7 2WS")
        self.driver.find_element(By.NAME, "postcode").send_keys("12-345")
        self.driver.find_element(By.NAME, "city").send_keys("Lenton")
        self.driver.find_element(By.NAME, "confirm-addresses").click()
        self.driver.find_element(By.NAME, "confirmDeliveryOption").click()
        self.driver.find_element(By.NAME, "conditions_to_approve[terms-and-conditions]").click()
        self.driver.find_element(by=By.ID, value="payment-confirmation").find_element(by=By.CLASS_NAME, value="btn-primary").click()

    def check_status(self):
        self.driver.find_element(By.CLASS_NAME, "account").click()
        self.driver.find_element(By.CLASS_NAME, "link-item").click()



if __name__ == "__main__":
    host = 'http://localhost:8080/index.php'
    tester = Tester(host)
    # test a
    # tester.add_to_cart_test("Karty graficzne AMD")
    # tester.add_to_cart_test("Płyty główne Socket AM4")

    # test b
    tester.search_test()

    # test c
    # tester.remove_3_from_cart()

    # test d
    tester.register()

    # test e
    tester.order()

    tester.driver.quit()