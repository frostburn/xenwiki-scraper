from os.path import exists
from pathlib import Path
import requests
from utils import Soup

Path("downloads/families").mkdir(parents=True, exist_ok=True)
Path("downloads/clans").mkdir(parents=True, exist_ok=True)
Path("downloads/subcategories").mkdir(parents=True, exist_ok=True)
Path("downloads/chromatic_realms").mkdir(parents=True, exist_ok=True)
Path("downloads/collections").mkdir(parents=True, exist_ok=True)


def download_page(url, filename):
    response = requests.get(url)

    with open(filename, "wb") as fp:
        for chunk in response.iter_content():
            fp.write(chunk)

base_url = "https://en.xen.wiki"

families_url = f"{base_url}/w/Category:Temperament_families"
families_filename = "downloads/Temperament_families.html"

if not exists(families_filename):
    print("downloading", families_url)
    download_page(families_url, families_filename)

with open(families_filename) as fp:
    soup = Soup(fp)

container = soup.find(class_="mw-category")

for anchor in container.find_all("a"):
    href = anchor.get("href")
    url = f"{base_url}{href}"
    name = href.split(":")[-1]
    filename = f"downloads/subcategories/{name}.html"
    if not exists(filename):
        print("downloading", url)
        download_page(url, filename)

container = soup.find_all(class_="mw-category")[1]

for anchor in container.find_all("a"):
    href = anchor.get("href")
    if href == "/w/Temperament_families_and_clans":
        continue
    url = f"{base_url}{href}"
    name = href.split("/")[-1]
    filename = f"downloads/families/{name}.html"
    if not exists(filename):
        print("downloading", url)
        download_page(url, filename)


clans_url = f"{base_url}/w/Category:Temperament_clans"
clans_filename = "downloads/Temperament_clans.html"

if not exists(clans_filename):
    print("downloading", clans_url)
    download_page(clans_url, clans_filename)

with open(clans_filename) as fp:
    soup = Soup(fp)

container = soup.find_all(class_="mw-category")[0]

for anchor in container.find_all("a"):
    href = anchor.get("href")
    if href == "/w/Temperament_families_and_clans":
        continue
    url = f"{base_url}{href}"
    name = href.split("/")[-1]
    filename = f"downloads/clans/{name}.html"
    if not exists(filename):
        print("downloading", url)
        download_page(url, filename)


chromatic_realms_url = f"{base_url}/w/Category:Commatic_realms"
chromatic_realms_filename = "downloads/Chromatic_realms.html"

if not exists(chromatic_realms_filename):
    print("downloading", chromatic_realms_url)
    download_page(chromatic_realms_url, chromatic_realms_filename)

with open(chromatic_realms_filename) as fp:
    soup = Soup(fp)

container = soup.find(class_="mw-content-ltr")

for anchor in container.find_all("a"):
    href = anchor.get("href")
    url = f"{base_url}{href}"
    name = href.split("/")[-1]
    filename = f"downloads/chromatic_realms/{name}.html"
    if not exists(filename):
        print("downloading", url)
        download_page(url, filename)


collections_url = f"{base_url}/w/Category:Temperament_collections"
collections_filename = "downloads/Temperament_collections.html"

if not exists(collections_filename):
    print("downloading", collections_url)
    download_page(collections_url, collections_filename)

with open(collections_filename) as fp:
    soup = Soup(fp)

container = soup.find_all(class_="mw-category")[1]

for anchor in container.find_all("a"):
    href = anchor.get("href")
    url = f"{base_url}{href}"
    name = href.split("/")[-1]
    filename = f"downloads/collections/{name}.html"
    if not exists(filename):
        print("downloading", url)
        download_page(url, filename)

chromatic_pairs_url = f"{base_url}/w/Chromatic_pairs"
chromatic_pairs_filename = "downloads/Chromatic_pairs.html"

if not exists(chromatic_pairs_filename):
    print("downloading", chromatic_pairs_url)
    download_page(chromatic_pairs_url, chromatic_pairs_filename)
