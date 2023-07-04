# product_file = "products.csv"
import csv
import string
import random
from woocommerce import API

wcapi = API(
    url="http://localhost:8888/localstore/",
    consumer_key="ck_",
    consumer_secret="cs_",
    version="wc/v3"
)


rs_api = wcapi.get("products", params={"per_page": 100, "page" : 1})
status_code = rs_api.status_code
# assert status_code == 200, f"Expected a '200' status code but got {status_code}"
# above code does exactly what below code does
if status_code != 200:
    raise Exception(f"Expected a '200' status code but got {status_code}")

# Set up additional products here
# This generates random product name to add to site
def generate_product_name(length=10):
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for _ in range(length))

# This generates a random price given a specified price range
def generate_product_price(min_price=20, max_price=400):
    return round(random.uniform(min_price, max_price))

# Add 200 products to website
for _ in range(2):
    product_data = {
        'name': generate_product_name(),
        'type': 'simple',
        'regular_price': str(generate_product_price())
    }

    wcapi.post("products", product_data).json()

# Add these products to a csv file with name and price as headers

all_products = rs_api.json()
filename = "all_products_02.csv"

with open(filename, "w", newline="") as csvfile:
    fieldnames = ["name", "price"]
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()

    for product in all_products:
        name = product["name"]
        price = product["price"]

        writer.writerow({"name": name, "price": price})


# for i in all_products:
#     print(i['name'],i['price'])

# breakpoint()