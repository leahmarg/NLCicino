import json
from pathlib import Path

import httpx
from bs4 import BeautifulSoup

initial_nlc_wine_url = "https://nlliquor.com/product-category/wine/"

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36"
}

nlc_products = []

next_url = initial_nlc_wine_url

page = 0
while next_url is not None:
    page += 1
    print(f"Getting page {page}")
    nlc_wine_html = httpx.get(next_url, headers=headers).text

    soup = BeautifulSoup(nlc_wine_html, "html.parser")

    for product in soup.select("li.product"):
        p_name = product.select_one("h2").get_text().strip()
        p_price = product.select_one("bdi").get_text().strip()
        p_info = product.select_one("div.meta-styles").get_text().strip()
        nlc_products.append(
            {
                "name": p_name,
                "price": p_price,
                "info": p_info,
            }
        )

    has_next_page = soup.select_one("a.next")

    if has_next_page is not None:
        next_url = has_next_page["href"]
    else:
        print("No more next page")
        next_url = None

print(f"Done, found {len(nlc_products)} products from NLC")

nlc_products_string = json.dumps(nlc_products, indent=4)
Path("nlc-products.json").write_text(nlc_products_string)

print("Written to nlc-products.json")
