import sys

from bs4 import BeautifulSoup
import requests
import lxml


def write_to_file(path, text):
    with open(path, 'w') as file:
        for line in text:
            file.write(line.text + "\n")


def get_page_text():
    url = "https://www.x-kom.pl/g-5/c/345-karty-graficzne.html"
    headers = {  # header mimicing web browser, so we dont get 403 response code
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    response = requests.get(url, headers=headers)

    if not response.ok:
        print("Error " + str(response))
        sys.exit()
    return response.text


def get_all_content(tag, html_class, searching_for):
    content = soup.find_all(tag, class_=html_class)
    if content:
        return content
    else:
        print(searching_for + "not found")
        sys.exit()

def get_one_content(tag, html_class, searching_for):
    content = soup.find(tag, class_=html_class)
    if content:
        return content
    else:
        print(searching_for + "not found")
        sys.exit()


global soup
if __name__ == "__main__":
    html_text = get_page_text()
    soup = BeautifulSoup(html_text, 'lxml')

    categories = get_all_content('span', 'sc-1fme39r-4 hkrryw', 'categories')
    with open('categoriesAndSubcategories', 'w') as file:
        for cat in categories:
            file.write(cat.text + ",")
        file.write("\n")

    products = get_all_content('div', 'sc-1s1zksu-0 dzLiED sc-162ysh3-1 irFnoT', 'products')
    with open('products', 'w') as file:
        for product in products:
            name = product.find('h3', class_="sc-16zrtke-0 kGLNun sc-1yu46qn-9 feSnpB")
            file.write(name.text + ",")
            attributes = product.find_all('li', 'sc-vb9gxz-2 ZaTQK')
            for att in attributes:
                file.write(att.text + ",")
            image = product.find('img')
            print(image['src'])
            file.write(image['src'])
            file.write("\n")

