import requests
from bs4 import BeautifulSoup
from extract import get_drupal_modules
from datetime import datetime
import concurrent.futures
from threading import Lock
from pprint import pprint

mutex = Lock()


def get_release_dates(composer_url: str):
    release_dates = {}
    thread_args = {}
    futures = []

    modules = get_drupal_modules(composer_url)
    executor = concurrent.futures.ThreadPoolExecutor(len(modules))
    for module in modules:
        future = executor.submit(get_latest_release_date, module)
        thread_args[future] = module
        futures.append(future)
    concurrent.futures.wait(futures)
    for future in futures:
        module = thread_args[future]
        release_date = future.result()
        release_dates[module] = release_date
    return release_dates


def get_latest_release_date(module: str) -> str:
    url = 'https://www.drupal.org/project/' + module
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'html.parser')
    releases = soup.find("span", class_='views-field views-field-created')
    if releases is None:
        return "N/A"
    raw_date = releases.find("span", class_='field-content').get_text()
    date_string = raw_date.removeprefix('released ')
    try:
        date_obj = datetime.strptime(date_string, '%d %B %Y')
    except ValueError:
        return "N/A"
    return date_obj.strftime("%Y-%m-%d")


file = 'https://raw.githubusercontent.com/govCMS/GovCMS/3.x-develop/composer.json'
pprint(get_release_dates(file))
