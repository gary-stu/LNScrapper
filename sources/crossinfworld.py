"""
TODO
"""
import re
from datetime import datetime
from logging import getLogger

import requests
from bs4 import BeautifulSoup

logger = getLogger(__name__)


def _get_webpage() -> BeautifulSoup | None:
    """
    TODO
    :return:
    """
    logger.debug('Querying Cross Infinite World new releases')
    webpage = requests.get('https://www.crossinfworld.com/Calendar.html')
    if webpage.status_code != 200:
        return

    return BeautifulSoup(webpage.text, "html.parser")


def _find_novels(soup: BeautifulSoup) -> list:
    """
    TODO
    :param soup:
    :return:
    """
    logger.debug('Parsing webpage')
    compiled_regexp = re.compile('Digital')
    releases = []

    table = soup.find('table')
    digital = table.find_all('td', text=compiled_regexp)

    for elem in digital:
        row = elem.parent
        children = list(row.find_all("td"))
        name = children[1].text
        date = datetime.strptime(children[3].text, '%m/%d/%y').strftime('%Y-%m-%d')
        serie = name.split(' Vol.')[0]

        new_release = {
            'date': date,
            'name': name,
            'serie': serie,
            'source': 'Cross Infinite World'
        }
        releases.append(new_release)

    return releases


def new_releases():
    """
    TODO
    :return:
    """
    logger.info('Fetching data from Cross Infinite World')
    soup = _get_webpage()
    if soup is None:
        return

    result = _find_novels(soup)
    logger.info('Fetched all required data from Cross Infinite World')
    return result
