"""
TODO
"""
from datetime import datetime
from logging import getLogger
from time import sleep

from bs4 import BeautifulSoup
from selenium.webdriver import Firefox
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By


logger = getLogger(__name__)
AJAX_WAIT_TIME = 3


def _get_webpage(
        driver: Firefox,
        year: int,
        month: int,
        day: int,
        sleep_time: int = AJAX_WAIT_TIME
) -> str:
    """
    TODO
    :param driver:
    :param year:
    :param month:
    :param day:
    :param sleep_time:
    :return:
    """
    url = f'https://yenpress.com/calendar?year={year}&month={month}&from_date={day}&layout=grid'

    logger.debug(f'Loading Yenpress calendar for {year}-{month}-{day}')
    driver.get(url)

    logger.debug('force load all ajax requests')
    driver.find_element(By.TAG_NAME, 'html').send_keys(Keys.END)

    logger.debug(f'Wait {sleep_time}s while ajax is being loaded')
    sleep(sleep_time)

    return driver.page_source


def _transform_webpages(webpages: list):
    """
    TODO
    :param webpages:
    :return:
    """
    logger.debug('transforming webpage source data into bs4 object')
    result = []
    for page in webpages:
        soup = BeautifulSoup(page, "html.parser")
        result.append(soup)

    return result


def _get_all_webpages(driver: Firefox) -> list:
    """
    TODO
    :param driver:
    :return:
    """
    today = datetime.utcnow()

    month_number = 0
    webpages = []

    year = today.year
    month = today.month
    day = today.day
    while month_number < 3:
        webpage = _get_webpage(driver, year, month, day)
        webpages.append(webpage)
        if month != 12:
            month += 1
        else:
            month = 1
            year += 1
        day = 1
        month_number += 1

    result = _transform_webpages(webpages)
    return result


def _find_novels(soup: BeautifulSoup, year: int, month: int) -> list:
    """
    TODO
    :param soup:
    :param year:
    :param month:
    :return:
    """
    novels = []
    releases = []

    # find all light novels
    elems = soup.find_all("span", class_="light-novels")
    for elem in elems:
        novels.append(elem.parent)

    # get data from each novel found
    for novel in novels:
        name = novel.find('h3').text
        name = name.split(' (light novel')[0]
        name = name.split(' (novel')[0]

        str_date = novel.find('p').text
        str_date = str_date.replace('\n', '')
        str_date = str_date.split()[0]
        try:
            int_date = int(str_date)
        except ValueError:
            int_date = 1
            logger.error('Could not get date as integer')
        release_date = datetime(year=year, month=month, day=int_date).strftime('%Y-%m-%d')

        new_release = {
            'name': name,
            'date': release_date,
            'serie': name.split(', Vol')[0],
            'source': 'Yenpress'
        }
        releases.append(new_release)

    return releases


def new_releases(driver: Firefox) -> list:
    """
    TODO
    :param driver:
    :return:
    """
    logger.info('Fetching data from Yenpress')
    soups = _get_all_webpages(driver)

    releases = []

    today = datetime.utcnow()
    year = today.year
    month = today.month

    for soup in soups:
        month_releases = _find_novels(soup, year, month)
        if month != 12:
            month += 1
        else:
            month = 1
            year += 1

        releases.extend(month_releases)

    logger.info('Fetched all required data from Yenpress')
    return releases
