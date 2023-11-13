import sys

from bs4 import BeautifulSoup
import requests


class Scrapper:
    def __init__(self):
        self.soup = BeautifulSoup()
        self.categoriesAndSubcategoriesFile = 'categoriesAndSubcategories.txt'
        self.productsFile = 'products.txt'
        self.url = ''
        self.current_category = ''

    def set_soup_from_page(self, url):
        self.url = url
        self.soup = BeautifulSoup(self.get_page_text(), 'lxml')

    def get_url_without_php(self):
        return self.url.split('?', 2)[0]

    def get_page_text(self):
        headers = {  # header mimicing web browser, so we dont get 403 response code
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                          "Chrome/91.0.4472.124 Safari/537.36"
        }
        response = requests.get(self.url, headers=headers)

        if not response.ok:
            print("Error " + str(response))
            sys.exit()
        return response.text

    def get_all_content(self, tag, html_class, searching_for):
        content = self.soup.find_all(tag, class_=html_class)
        if content:
            return content
        else:
            print(searching_for + "not found in" + self.url)
            sys.exit()

    def get_one_content(self, tag, html_class, searching_for):
        content = self.soup.find(tag, class_=html_class)
        if content:
            return content
        else:
            print(searching_for + "not found in" + self.url)
            sys.exit()

    def get_page_count(self):
        text = self.get_one_content('span', 'sc-11oikyw-2 fUaLpF', 'page count').text
        return int(text.split(' ')[1])

    def append_categories_to_file(self):
        categories = [cat.text for cat in self.get_all_content('span', 'sc-1fme39r-4 hkrryw', 'categories')]
        self.current_category = categories[0]
        with open(self.categoriesAndSubcategoriesFile, 'a', encoding="UTF-8") as file:
            file.write(','.join(categories) + "\n")

    def append_products_to_file(self):
        page_count = scrapper.get_page_count()
        for page_number in range(page_count):
            page_php = "?page=" + str(page_number + 1)
            self.set_soup_from_page(self.get_url_without_php() + page_php)
            products = scrapper.get_all_content('div', 'sc-1s1zksu-0 dzLiED sc-162ysh3-1 irFnoT', 'products')
            with open(self.productsFile, 'a', encoding="UTF-8") as file:
                for product in products:
                    image = product.find('img')
                    # if image is a svg, product is unavailable, so it's ignored
                    if image['src'][-4:] != ".svg":
                        print(image['src'])
                        name = product.find('h3', class_='sc-16zrtke-0 kGLNun sc-1yu46qn-9 feSnpB')
                        file.write(self.current_category + "," + name.text + ",")
                        attributes = [attribute.text for attribute in product.find_all('li', 'sc-vb9gxz-2 ZaTQK')]
                        file.write(','.join(attributes))
                        file.write(',' + image['src'])
                        file.write("\n")

        self.set_soup_from_page(self.get_url_without_php())

    def clear_files(self):
        with open(self.categoriesAndSubcategoriesFile, 'w', encoding="UTF-8"):
            pass
        with open(self.productsFile, 'w', encoding="UTF-8"):
            pass

    def scrape(self, url):
        self.set_soup_from_page(url)
        self.append_categories_to_file()
        self.append_products_to_file()


if __name__ == "__main__":
    scrapper = Scrapper()
    host = 'https://www.x-kom.pl/'
    paths = ["g-5/c/345-karty-graficzne.html",
             "g-4/c/1663-tablety.html",
             "g-5/c/89-dyski-twarde-hdd-i-ssd.html",
             "g-6/c/15-monitory.html"]

    scrapper.clear_files()
    for path in paths:
        scrapper.scrape(host + path)
