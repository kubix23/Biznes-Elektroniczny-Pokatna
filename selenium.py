from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
class Tester:
    def __init__(self, url):
        self.url = url
        self.driver = webdriver.Chrome()
        self.driver.get(self.url)

    def add_to_cart_test(self):
        collapse_menu = self.driver.find_element(by=By.CLASS_NAME, value="collapse")
        action = ActionChains(driver=self.driver)
        #action.MoveToElement(element).Perform();
#        collapse_menu.click()
        show_button = self.driver.find_element(by=By.CLASS_NAME, value="collapse # quick-view js-quick-view")
        show_button.click()
        add_button = self.driver.find_element(by=By.CLASS_NAME, value="btn btn-primary add-to-cart")
        add_button.click()

        # for _ in range(2):
        #     adder = Tester("http://localhost:8080/index.php?id_category=1742&controller=category")
        #     adder.driver.implicitly_wait(0.5)
        #     show_button = adder.driver.find_element(by=By.CLASS_NAME, value="quick-view js-quick-view")
        #     show_button.click()
        #     add_button = adder.driver.find_element(by=By.CLASS_NAME, value="btn btn-primary add-to-cart")
        #     add_button.click()


if __name__ == "__main__":
    host = 'http://localhost:8080/index.php'
    tester = Tester(host)
    tester.add_to_cart_test()
    tester.driver.quit()
