import json
from pathlib import Path

import httpx

url = "https://www.vivino.com/api/explore/explore"
params = {
    "country_code": "ca",
    "currency_code": "CAD",
    "facets": "true",
    "grape_filter": "varietal",
    "min_rating": "1",
    "order_by": "price",
    "order": "asc",
    "price_range_max": "500",
    "price_range_min": "0",
    "wine_type_ids[]": [1, 2, 3, 4, 7, 24],
    "page": 1,
}

headers = {
    "accept": "application/json",
    "content-type": "application/json",
}

vivino_products = []
total_records = None
seen_records = 0
page = 0

with httpx.Client() as client:
    while total_records is None or seen_records <= total_records:
        page += 1

        print(f"On page {page}, seen {seen_records} of {total_records}")

        response = client.get(url, params=params, headers=headers)
        data = response.json()["explore_vintage"]
        records = data["records"]
        if total_records is None:
            total_records = data["records_matched"]

        for record in records:
            seen_records += 1
            name = record["vintage"]["name"]
            sku = record["price"]["sku"]
            image = record["vintage"]["image"]["location"]
            vivino_products.append(
                {
                    "name": name,
                    "sku": sku,
                    "image": image,
                    "record": record,
                }
            )
        params["page"] += 1

print("Done fetching vivino products")

vivino_products_string = json.dumps(vivino_products, indent=4)
Path("vivino-products.json").write_text(vivino_products_string)

print("Written to vivino-products.json")
