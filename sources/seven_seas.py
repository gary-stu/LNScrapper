"""
TODO
"""
import re
from datetime import datetime
from logging import getLogger
from time import sleep

from bs4 import BeautifulSoup
from selenium.webdriver import Firefox

logger = getLogger(__name__)


def _get_webpage(driver: Firefox) -> BeautifulSoup | None:
    """

    :param driver:
    :return:
    """
    url = 'https://sevenseasentertainment.com/release-dates'
    logger.debug('Loading Seven Seas calendar')
    driver.get(url)
    sleep(1)

    logger.debug('Ensure loading worked properly')
    page_source = driver.page_source
    if 'Coming Soon' not in page_source:
        logger.error('Browser may have been detected as bot')
        return

    logger.debug('Converting page source to bs4 object')
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    return soup


def _find_novels(webpage: BeautifulSoup) -> list:
    """
    TODO
    :param webpage:
    :return:
    """
    logger.debug('Parsing webpage to find new releases')
    novels = []
    compiled_regexp = re.compile('Light Novel')

    table = webpage.find('table', id='releasedates')
    novels_td = table.find_all('td', text=compiled_regexp)

    for elem in novels_td:
        row = elem.parent
        children = list(row.find_all())

        date = datetime.strptime(children[0].text, '%Y/%m/%d').strftime('%Y-%m-%d')
        name = children[3].text
        serie = name.split(' Vol.')[0]
        serie = serie.split(' (Light Novel')[0]

        new_release = {
            'name': name,
            'date': date,
            'serie': serie,
            'source': 'Seven Seas'
        }
        novels.append(new_release)

    return novels


def new_releases(driver: Firefox) -> list:
    """
    TODO
    :param driver:
    :return:
    """
    logger.info('Fetching data from Seven Seas')
    webpage = _get_webpage(driver)

    if webpage is None:
        return []

    releases = _find_novels(webpage)
    logger.info('Fetched all required data from Seven Seas')
    return releases
