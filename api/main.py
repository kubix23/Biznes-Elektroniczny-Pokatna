import random
from multiprocessing.pool import ThreadPool

from threading import Semaphore
from prestapyt import PrestaShopWebServiceDict
import pandas as pd

prestashop = PrestaShopWebServiceDict('http://localhost:8080/api', "U5R1TNFG9QL2ZF544CU69R5XP2TUKVJG")
semaphore = Semaphore(1)

def addCategory(name, parent=2):
    category_schema = prestashop.get("categories", options={"schema": "blank"})
    category_schema["category"]["name"]["language"]["value"] = name
    category_schema["category"]["id_parent"] = parent
    category_schema["category"]["active"] = 1
    category_schema["category"]["description"]["language"]["value"] = f"Kategoria {name}"
    category_schema["category"]["link_rewrite"]["language"]["value"] = "test"
    return prestashop.add("categories", category_schema)["prestashop"]["category"]["id"]


def addFeature(atribute):
    res = []
    for temp in atribute:

        name = temp.split(":")[0]
        value = temp.split(":")[1]
        feature_values_schema = prestashop.get("product_feature_values", options={"schema": "blank"})
        feature_schema = prestashop.get("product_features", options={"schema": "blank"})
        semaphore.acquire()
        feature = prestashop.get("product_features", options={"filter[name]": name})
        if feature["product_features"]:
            feature_id = feature["product_features"]["product_feature"]["attrs"]["id"]
        else:
            feature_schema["product_feature"]["name"]["language"]["value"] = name
            feature_id = prestashop.add("product_features", feature_schema)["prestashop"]["product_feature"]["id"]

        feature_values_schema["product_feature_value"]["id_feature"] = feature_id
        feature_values_schema["product_feature_value"]["value"]["language"]["value"] = value
        feature_values_schema["product_feature_value"]["custom"] = 0
        feature_values_id = \
            prestashop.add("product_feature_values", feature_values_schema)["prestashop"]["product_feature_value"]["id"]
        res.append((feature_id, feature_values_id))
        semaphore.release()

    return res


def addProduct(product):
    features = addFeature(product[3:6])
    product_schema = prestashop.get("products", options={"schema": "blank"})
    category_id = prestashop.get("categories", options={
        "filter[name]": product[0]})["categories"]["category"]["attrs"]["id"]
    del product_schema["product"]["position_in_category"]
    product_schema["product"]["manufacturer"] = product[1].split(" ", 1)[0]
    product_schema["product"]["name"]["language"]["value"] = product[1]
    product_schema["product"]["id_category_default"] = category_id
    product_schema["product"]["price"] = random.randint(10, 4000)
    product_schema["product"]["id_shop_default"] = 1
    product_schema["product"]["active"] = 1
    product_schema["product"]["state"] = 1
    product_schema["product"]["available_for_order"] = 1
    product_schema["product"]["minimal_quantity"] = 1
    product_schema["product"]["show_price"] = 1
    product_schema["product"]["weight"] = random.randint(1, 60) / 10
    product_schema["product"]["associations"]["categories"] = {
        "category": [
            {"id": 2},
            {"id": category_id}
        ],
    }

    product_features = []
    for feature_id, value_id in features:
        product_features.append({
            "id": feature_id,
            "id_feature_value": value_id
        })
    # product_schema["product"]["associations"]["product_features"]["product_feature"] = product_features
    product_id = prestashop.add("products", product_schema)["prestashop"]["product"]["id"]

    schema_id = prestashop.search("stock_availables", options={"filter[id_product]": product_id})[0]
    stock_available = prestashop.get("stock_availables", resource_id=schema_id)
    stock_available["stock_available"]["quantity"] = random.randint(0, 30)
    stock_available["stock_available"]["depends_on_stock"] = 0
    prestashop.edit("stock_availables", stock_available)


# delete category
ids = []
for category in prestashop.get("categories")["categories"]["category"]:
    if int(category["attrs"]["id"]) not in [1, 2]:
        ids.append(int(category["attrs"]["id"]))
if ids:
    print("Deleting categories...")
    prestashop.delete("categories", resource_ids=ids)

# add category
csvfile = pd.read_csv('../ScraperResults/categoriesAndSubcategories.txt', names=range(10), sep=';')
for i in range(len(csvfile)):
    id = addCategory(csvfile[0][i])
    for j in csvfile.T[i].dropna()[1:]:
        addCategory(j, id)

# remove products
products = prestashop.get("products")["products"]
if products:
    products_data = products["product"]

    if isinstance(products_data, dict):
        products_data = [products_data]

    ids = [int(product["attrs"]["id"]) for product in products_data]
    if ids:
        print("Deleting products...")
        prestashop.delete("products", resource_ids=ids)

# remove products
features = prestashop.get("product_features")["product_features"]
if features:
    features_data = prestashop.get("product_features")[
        "product_features"]["product_feature"]

    if isinstance(features_data, dict):
        features_data = [features_data]

    ids = [int(feature["attrs"]["id"]) for feature in features_data]
    if ids:
        print("Deleting features...")
        prestashop.delete("product_features", resource_ids=ids)

# add products

pool = ThreadPool(20)
csvfile = pd.read_csv('../ScraperResults/products.txt', header=None, sep=';')
csvfile = csvfile.drop(0, axis=1)
pool.map(addProduct, csvfile.values)
pool.close()
pool.join()
