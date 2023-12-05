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

    def add_to_cart_test(self):
        collapse_menu = self.driver.find_element(by=By.CLASS_NAME, value="top-menu")
        action = ActionChains(driver=self.driver)
        action.move_to_element(collapse_menu).perform()
        cat1 = self.driver.find_element(by=By.LINK_TEXT, value="Karty graficzne AMD")
        action.move_to_element(cat1).click().perform()

        for i in range(5):
            products = self.driver.find_elements(by=By.CLASS_NAME, value="product-description")
            print(products[i].text)
            products[i].click()
            # WebDriverWait(self.driver, 3).until(EC.element_to_be_clickable((By.CLASS_NAME,"btn btn-primary add-to-cart"))).click()
            # self.driver.implicitly_wait(3)

            action.move_to_element(self.driver.find_element(by=By.XPATH, value="//*[@id=\"add-to-cart-or-refresh\"]/div[2]/div/div[2]/button")).click().perform()

            # action.click().perform()
            self.driver.back()
if __name__ == "__main__":
    #host = 'http://localhost:8080/index.php'
    host = 'file:///home/khasar/Desktop/Karty%20graficzne%20NVIDIA.html'
    tester = Tester(host)
    tester.add_to_cart_test()
    tester.driver.quit()
