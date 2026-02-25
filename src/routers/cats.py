import json
import re
from pathlib import Path

from fastapi import APIRouter, Depends, HTTPException, Request, status
from fastapi.security import APIKeyHeader

from src.schemas.schemas import Cat
from src.utils.utils import get_logger

router = APIRouter()
logger = get_logger("routes")

# Python excpects the files to be in the current working dir where you call the app.
BASE_DIR = Path(__file__).resolve().parent.parent
CATS_FILE = BASE_DIR / "cats.json"

API_KEYS = {"secret_key_1", "my-secret-key"}

api_key_header = APIKeyHeader(name="X-API-Key", auto_error=False)


async def validate_api_key(x_api_key: str = Depends(api_key_header)):
    """
    Validates the API key provided in the X-API-Key header.
    """
    if x_api_key is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="API key not provided"
        )
    if x_api_key not in API_KEYS:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid API Key"
        )
    return x_api_key  # You can return a user object or user ID here


# with open(CATS_FILE, "r") as file:
#     data = json.load(file)

# cat_dict = {}
# cat_id = 0
# # standardize the data
# for value in data.values():
#     toy_name_underscore = re.sub(" ", "_", value["favorite_toy"].lower())
#     print(toy_name_underscore)
#     value["favorite_toy"] = toy_name_underscore
#     cat_id += 1
#     cat_dict[cat_id] = value
# print(cat_dict)
# with open(CATS_FILE, "w") as file:
#     json.dump(cat_dict, file, indent=4)

# # get unique breeds
# cat_filtered = {}
# cat_filtered_list = []
# for key, value in data.items():
#     cat_filtered_list.append(value["breed"])
#     unique_breeds = list(set(cat_filtered_list))
# print(unique_breeds)

# use dict of dicts to load in data
# but use a list of dicts to return data via query parameters for filtering

def read_data(filename=CATS_FILE):
    with open(filename, "r") as file:
        return json.load(file)


def save_data(data):
    with open(CATS_FILE, "w") as file:
        json.dump(data, file, indent=4)


def dict_to_list(cat_dict):
    total_records_to_return = []
    for key, record in cat_dict.items():
        total_records_to_return.append(record)
    return total_records_to_return


def filter_cats(cat_dict, desired_breed, desired_age, desired_toy):
    logger.info(
        f"filtering for breed={desired_breed}, age={desired_age}, toy={desired_toy}"
    )
    filtered_cats = {}
    for key, value in cat_dict.items():
        if desired_breed != None and value["breed"] != desired_breed:
            continue
        if desired_age != None and value["age"] != desired_age:
            continue
        if desired_toy != None and value["favorite_toy"] != desired_toy:
            continue
        filtered_cats[key] = value
    return filtered_cats

def build_page_url(request: Request, page_num: int, page_size: int, breed, age, favorite_toy):
    params = {
        "page_num": page_num,
        "page_size": page_size,
    }

    if breed is not None:
        params["breed"] = breed

    if age is not None:
        params["age"] = age

    if favorite_toy is not None:
        params["favorite_toy"] = favorite_toy

    url = request.url.include_query_params(**params)
    return str(url)

@router.get("/cats")
def get_cats(
    request: Request,
    page_num: int = 1,
    page_size: int = 10,
    breed: str = None,
    age: int = None,
    favorite_toy: str = None,
):
    # print(page_num, page_size, breed, age, favorite_toy)
    logger.info(f"Request for: {request.url}")
    start = (page_num - 1) * page_size
    end = start + page_size
    data = read_data()

    if breed or age or favorite_toy:
        filtered_cats = filter_cats(data, breed, age, favorite_toy)
    else:
        filtered_cats = data

    list_of_cats = dict_to_list(filtered_cats)
    filtered_length = len(list_of_cats)
    page_items = list_of_cats[start:end]

    next_page = None
    if end < filtered_length:
        next_page = build_page_url(request, page_num + 1, page_size, breed, age, favorite_toy)

    prev_page = None
    if page_num > 1:
        prev_page = build_page_url(request, page_num - 1, page_size, breed, age, favorite_toy)

    response = {
        # the actual data
        "data": page_items,
        # the total amount of data across all pages
        "total": filtered_length,
        # the amount of data returned in the current page
        "count": len(page_items),
        "pagination": {"next": next_page, "previous": prev_page},
    }

    if start >= filtered_length:
        response["data"] = 0
        response["pagination"]["next"] = "none"
        response["pagination"]["previous"] = "none"
    logger.info(f"Returning response with {len(page_items)} items")
    return response


@router.post("/cats")
def create_cat(cat: Cat):
    # convert Pydantic model → dictionary
    cat_dict = cat.model_dump()
    data = read_data()
    data_length = len(data)

    # Stadardize the data before saving it to the file.
    favorite_toy =cat_dict.pop("favorite_toy")
    favorite_toy_standardized = re.sub(" ", "_", favorite_toy.lower())
    cat_dict["favorite_toy"] = favorite_toy_standardized

    data[data_length + 1] = cat_dict
    save_data(data)

    print(cat_dict)

    return {
        "message": "Cat added successfully",
        "cat_id": (data_length + 1),
        "cat": cat_dict,
    }


@router.delete("/cats/{cat_id}", dependencies=[Depends(validate_api_key)])
def delete_cat(cat_id: str):
    data = read_data()
    removed_cat = data.pop(cat_id, None)
    if removed_cat is None:
        # Set custom 404 message for resource not found.
        raise HTTPException(status_code=404, detail="Cat not found")
    else:
        save_data(data)
        return {"message": "Cat successfully removed", "cat": removed_cat}
