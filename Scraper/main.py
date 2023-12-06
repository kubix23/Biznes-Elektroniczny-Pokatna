import sys

from bs4 import BeautifulSoup
import requests


class Scraper:
    def __init__(self, host_url):
        self.soup = BeautifulSoup()
        self.categoriesAndSubcategoriesFile = '../ScraperResults/categoriesAndSubcategories.txt'
        self.productsFile = '../ScraperResults/products.txt'
        self.url = ''
        self.host = host_url
        self.current_category = ''
        self.product_page_scraper = None

    def set_host(self, host_url):
        self.host = host_url

    def set_soup_from_page(self, url):
        self.url = url
        self.soup = BeautifulSoup(self.get_page_text(), 'lxml')

    def get_url_without_php(self):
        return self.url.split('?', 2)[0]

    def get_page_text(self):
        headers = {  # header mimicking web browser, so we dont get 403 response code
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
            print(searching_for + " not found in" + self.url)
            sys.exit()

    def get_page_count(self):
        text = self.get_one_content('span', 'sc-11oikyw-2 fUaLpF', 'page count').text
        return int(text.split(' ')[1])

    def append_categories_to_file(self):
        categories = [cat.text for cat in self.get_all_content('span', 'sc-1fme39r-4 hkrryw', 'categories')]
        self.current_category = categories[0]
        print(self.current_category)
        with open(self.categoriesAndSubcategoriesFile, 'a', encoding="UTF-8") as file:
            file.write(';'.join(categories) + "\n")

    def scrape_product_page(self, url):
        self.product_page_scraper.set_host(url)
        self.product_page_scraper.set_soup_from_page(url)
        span = self.product_page_scraper.get_one_content('span',
                                                         'sc-1tblmgq-0 sc-1tblmgq-3 cIswgX sc-jiiyfe-2 jGSlBb',
                                                         'image')
        image = span.find('img', class_='sc-1tblmgq-1 fatMoG')['src']
        page_title = self.product_page_scraper.soup.find('title')
        subcategory = page_title.text.split(" - ")[-3]
        desc_section = self.product_page_scraper.soup.find('section',class_='product-description content product-page')
        try:
            desc_candidate_1 = desc_section.find_all('p')[1].text
            desc_candidate_2 = desc_section.find_all('p')[2].text
            desc_candidate_3 = desc_section.find_all('p')[3].text
            desc = desc_candidate_1
            if len(desc_candidate_2.strip()) > len(desc.strip()):
                desc = desc_candidate_2
            if len(desc_candidate_3.strip()) > len(desc.strip()):
                desc = desc_candidate_3
            short_desc = desc.split('.')[0]
        except:
            desc = "Brak opisu na stronie x-kom"
            short_desc = desc
        print(desc)
        print("-------")
        return image, subcategory, desc, short_desc

    def append_products_to_file(self):
        page_count = self.get_page_count()
        self.product_page_scraper = Scraper("")

        with open(self.productsFile, 'a', encoding="UTF-8") as file:
            for page_number in range(page_count):
                page_php = "?page=" + str(page_number + 1)
                self.set_soup_from_page(self.get_url_without_php() + page_php)
                products = self.get_all_content('div', 'sc-1s1zksu-0 dzLiED sc-162ysh3-1 irFnoT', 'products')
                for product in products:
                    small_image = product.find('img')['src']
                    is_available = small_image[-4:] != ".svg"
                    # if image is a svg, product is unavailable, so it's ignored
                    if is_available:
                        product_url = host + product.find('a')['href'][1:]
                        image, subcategory, desc, short_desc = self.scrape_product_page(product_url)
                        name = product.find('h3', class_='sc-16zrtke-0 kGLNun sc-1yu46qn-9 feSnpB')
                        attributes = [attribute.text for attribute in product.find_all('li', 'sc-vb9gxz-2 ZaTQK')]
                        file.write(self.current_category + ";" + subcategory + ";" + name.text + ";" +
                                   ';'.join(attributes) + ';' + small_image + ';' + image + ';' + desc + ';' + short_desc + "\n")

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
    host = 'https://www.x-kom.pl/'
    paths = ["g-6/c/4051-drukarki-ze-skanerem.html",
             "g-4/c/1663-tablety.html",
             "g-5/c/14-plyty-glowne.html",
             "g-5/c/345-karty-graficzne.html"]
    scraper = Scraper(host)

    scraper.clear_files()
    for path in paths:
        scraper.scrape(host + path)
