from os.path import exists
from pathlib import Path
import requests
from utils import Soup

Path("downloads/families").mkdir(parents=True, exist_ok=True)
Path("downloads/subcategories").mkdir(parents=True, exist_ok=True)


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
