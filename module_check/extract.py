import re
import requests

exceptions = {
    "consultation-consultation": "consultation",
}


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
