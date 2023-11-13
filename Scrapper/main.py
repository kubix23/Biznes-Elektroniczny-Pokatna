import sys

from bs4 import BeautifulSoup
import requests


class Scrapper:
    def __init__(self):
        self.soup = BeautifulSoup()
        self.categoriesAndSubcategoriesFile = 'categoriesAndSubcategories'
        self.productsFile = 'products'
        self.url = ''

    def set_soup_from_page(self, url):
        self.url = url
        self.soup = BeautifulSoup(self.get_page_text(url), 'lxml')

    def get_url_without_php(self):
        return self.url.split('?', 2)[0]

    @staticmethod
    def get_page_text(url):

        headers = {  # header mimicing web browser, so we dont get 403 response code
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                          "Chrome/91.0.4472.124 Safari/537.36"
        }
        response = requests.get(url, headers=headers)

        if not response.ok:
            print("Error " + str(response))
            sys.exit()
        return response.text

    def get_all_content(self, tag, html_class, searching_for):
        content = self.soup.find_all(tag, class_=html_class)
        if content:
            return content
        else:
            print(searching_for + "not found")
            sys.exit()

    def get_one_content(self, tag, html_class, searching_for):
        content = self.soup.find(tag, class_=html_class)
        if content:
            return content
        else:
            print(searching_for + "not found")
            sys.exit()

    def get_page_count(self):
        text = self.get_one_content('span', 'sc-11oikyw-2 fUaLpF', 'page count').text
        return int(text.split(' ')[1])

    def append_categories_to_file(self):
        categories = self.get_all_content('span', 'sc-1fme39r-4 hkrryw', 'categories')
        with open(self.categoriesAndSubcategoriesFile, 'a') as file:
            for cat in categories:
                file.write(cat.text + ",")
            file.write("\n")

    def append_products_to_file(self):
        page_count = scrapper.get_page_count()
        for page_number in range(page_count):
            page_php = "?page=" + str(page_number + 1)
            self.set_soup_from_page(self.get_url_without_php() + page_php)
            products = scrapper.get_all_content('div', 'sc-1s1zksu-0 dzLiED sc-162ysh3-1 irFnoT', 'products')
            with open(self.productsFile, 'a') as file:
                for product in products:
                    name = product.find('h3', class_='sc-16zrtke-0 kGLNun sc-1yu46qn-9 feSnpB')
                    file.write(name.text + ",")
                    attributes = product.find_all('li', 'sc-vb9gxz-2 ZaTQK')
                    for att in attributes:
                        file.write(att.text + ",")
                    image = product.find('img')
                    print(image['src'])
                    file.write(image['src'])
                    file.write("\n")

    def clear_files(self):
        with open(self.categoriesAndSubcategoriesFile, 'w'):
            pass
        with open(self.productsFile, 'w'):
            pass


if __name__ == "__main__":
    scrapper = Scrapper()
    host = 'https://www.x-kom.pl/'
    path = 'g-5/c/345-karty-graficzne.html'
    scrapper.clear_files()

    scrapper.set_soup_from_page(host + path)
    scrapper.append_categories_to_file()
    scrapper.append_products_to_file()
