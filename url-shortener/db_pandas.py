import pandas as pd
import numpy as np
BASE62 = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"


# functions for deleting dataset or a specific url data
def delete_data():
    new_dataset = pd.DataFrame({"original_url": [], "short_url": []})
    new_dataset.to_csv("./data/urls.csv", index=False)


def delete_url(short_url):
    urls = pd.read_csv("./data/urls.csv", dtype={"original_url": object, "short_url": object})
    urls = urls[urls["short_url"] != short_url]
    urls.to_csv("./data/urls.csv", index=False)


# function for posting the original_url and the generated short_url into database
def add_url(original_url):
    urls = pd.read_csv("./data/urls.csv", dtype={"original_url": object, "short_url": object})
    # if url does not exist in database, add new url to the database
    if not (if_url_exists(original_url, urls)):
        # generate short_url, original_url -> id -> base62-short_url
        short_url = get_short_url(original_url)
        the_url = pd.DataFrame({"original_url": [str(original_url)], "short_url": [str(short_url)]})
        new_urls = pd.concat([urls, the_url], ignore_index=True)
        new_urls.to_csv("./data/urls.csv", index = False)
    # if url exists in database, do not post
    else:
        print("url exists")


def if_url_exists(original_url, urls):
    return urls["original_url"].str.contains(original_url).any()


# generate short url
def get_short_url(original_url):
    index = get_url_index(original_url)
    short_url = encode(index, alphabet=BASE62)
    return short_url


def get_url_index(original_url):
    urls = pd.read_csv("./data/urls.csv", dtype={"original_url": object, "short_url": object})
    # url exists
    if if_url_exists(original_url, urls):
        exist_index = urls[urls["original_url" == original_url]].index
        return exist_index
    # url does not exist, get the prospected auto-incremented index
    else:
        return urls.index.size


# function for getting original_url from short_url in db
def get_url(short_url):
    urls = pd.read_csv("./data/urls.csv", dtype={"original_url": object, "short_url": object})
    original_url = urls[urls["short_url"] == short_url]["original_url"].tolist()[0]
    return original_url


# function for getting short url from original url in db
def get_short_url_fromDB(original_url):
    urls = pd.read_csv("./data/urls.csv", dtype={ "original_url" : object, "short_url": object})
    short_url = urls[urls["original_url"] == original_url]["short_url"].tolist()[0]
    return short_url


def get_all_urls():
    urls = pd.read_csv("./data/urls.csv", dtype={"original_url": object, "short_url": object})
    return urls


def encode(num, alphabet=BASE62):
    if num == 0:
        return alphabet[0]
    arr = []
    base = len(alphabet)
    while num:
        num, rem = divmod(num, base)
        arr.append(alphabet[rem])
    arr.reverse()
    return ''.join(arr)
