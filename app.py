import os
import csv
import requests
from urllib.parse import urljoin
from dataclasses import dataclass, fields, astuple


# here goes your api_key from
# https://www.yelp.com/developers/v3/manage_app
API_KEY = ""

API_HOST = "https://api.yelp.com"
SEARCH_PATH = "/v3/businesses/search"

# city location to start search
BASE_LOCATION = "Vancouver BC"

# name of the directory to pile up result files
RESULTS_DIR = "results"


# model of a single output item
# every field will be corresponding column in result file
@dataclass
class BusinessItem:
    name: str
    page: str
    telephone: str
    search_category: str
    yelp_categories: str
    rating: float
    reviews: int
    search_address: str
    address: str
    post_code: str
    city: str
    country: str
    state: str


def search_request(search_address: str, search_category: str):
    full_path = urljoin(API_HOST, SEARCH_PATH)
    full_address = BASE_LOCATION + search_address
    headers = {
        "Authorization": f"Bearer {API_KEY}",
    }
    url_params = {
        "term": search_category.replace(" ", "+"),
        "location": full_address.replace(" ", "+"),
    }
    response = requests.get(full_path, headers=headers, params=url_params)

    return response.json()


def parse_address(location: dict) -> str:
    _search_fields = ("address1", "address2", "address3")
    full_address = []
    for field in _search_fields:
        if location[field]:
            full_address.append(location[field])
    return " ".join(full_address)


def get_single_item(item: dict, search_address: str, search_category: str) -> dataclass:
    return BusinessItem(
        name=item["name"],
        page=item["url"],
        telephone=item["display_phone"],
        search_category=search_category,
        yelp_categories= ", ".join((category["title"] for category in item["categories"])),
        rating=item["rating"],
        reviews=item["review_count"],
        search_address=search_address,
        address=parse_address(item["location"]),
        post_code=item["location"]["zip_code"],
        city=item["location"]["city"],
        country=item["location"]["country"],
        state=item["location"]["state"],
    )


def get_businesses(search_address: str, search_category: str) -> list[dataclass]:
    response = search_request(search_address, search_category)
    businesses_found = [get_single_item(
            item,
            search_address,
            search_category
        ) for item in response["businesses"]
    ]
    return businesses_found


def write_to_csv_file(items: list[dataclass], filename: str) -> None:
    fields_ = [field.name for field in fields(items[0])]
    with open(os.path.join(RESULTS_DIR, filename), "w") as file:
        writer = csv.writer(file)
        writer.writerow(fields_)
        writer.writerows((astuple(item) for item in items))


def main(search_address: str, search_category: str) -> None:
    result_found = get_businesses(search_address, search_category)

    os.makedirs(RESULTS_DIR, exist_ok=True)
    output_file_name = (
        f"{search_address.lower().replace(' ', '_')}_"
        f"{search_category.lower().replace(' ', '_')}.csv"
    )
    write_to_csv_file(result_found, output_file_name)


if __name__ == "__main__":
    search_address = "Coal Harbor"
    search_category = "eyelash"

    main(search_address, search_category)
