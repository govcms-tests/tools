from bs4 import BeautifulSoup
from datetime import datetime
from concurrent.futures import wait, ThreadPoolExecutor
from typing import TypedDict
from pprint import pprint
from threading import Lock

import requests
import parse
import re


exceptions = {
    "consultation-consultation": "consultation",
}


mutex = Lock()


def get_drupal_modules(composer_url: str) -> list[str]:
    data = requests.get(composer_url).json()
    drupal_modules = []
    for key, value in data['require'].items():
        # Only consider drupal modules.
        if not re.search("^drupal/.*", key):
            continue
        name = key.removeprefix('drupal/')
        if name in exceptions:
            drupal_modules.append(exceptions[name])
            continue
        drupal_modules.append(name)
    return drupal_modules


def get_number_open_bugs(html: BeautifulSoup) -> int:
    html_filtered = html.find('div', class_="issue-cockpit-1").find('a')
    bugs_open_string = html_filtered.get_text()
    format = '{:d} open'
    bugs_open = parse.parse(format, bugs_open_string)[0]
    return bugs_open


def get_last_release(html: BeautifulSoup) -> datetime:
    releases = html.find("span", class_='views-field views-field-created')
    if releases is None:
        return "N/A"
    raw_date = releases.find("span", class_='field-content').get_text()
    date_string = raw_date.removeprefix('released ')
    try:
        date = datetime.strptime(date_string, '%d %B %Y')
    except ValueError:
        print("Unable to convert: ", date_string)
        return None
    return date


def get_last_dev_update(html: BeautifulSoup) -> datetime:
    filtered = html.find('div', class_="release-info").find('p').find('small')
    update_string = filtered.get_text()
    if date_search := re.search('updated (.*) at (.*)', update_string):
        date_string = date_search.group(1)
    else:
        raise ValueError
    return datetime.strptime(date_string, '%d %b %Y')


def get_module_page(module: str) -> BeautifulSoup:
    print('Getting page for: ', module)
    url = 'https://www.drupal.org/project/' + module
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'html.parser')
    return soup


def get_module_pages(modules: list[str]) -> dict[str, BeautifulSoup]:
    module_pages = {}
    futures = []
    executor = ThreadPoolExecutor(len(modules))
    for module in modules:
        future = executor.submit(get_module_page, module)
        module_pages[module] = future.result()
        futures.append(future)
    wait(futures)
    return module_pages


class ModuleInfo(TypedDict):
    last_release_date: datetime
    last_commit_date: datetime


def extract_module_info(page: BeautifulSoup) -> ModuleInfo:
    release_date = get_last_release(page)
    commit_date = get_last_dev_update(page)
    return {'last_release_date': release_date, 'last_commit_date': commit_date}


def get_module_info(pages: dict[str, BeautifulSoup]) -> dict[str, ModuleInfo]:
    info = {}
    for module_name, module_page in pages.items():
        info[module_name] = extract_module_info(module_page)
    return info


url = 'https://raw.githubusercontent.com/govCMS/GovCMS/3.x-develop/composer.json'
modules = get_drupal_modules(url)
pages = get_module_pages(modules)
module_info = get_module_info(pages)
pprint(module_info)
