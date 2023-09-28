"""
TODO
"""
from datetime import datetime
from logging import getLogger

import requests

logger = getLogger(__name__)

DATE_FORMAT = '%Y-%m-%dT%H:%M:%SZ'


def _get_new_releases() -> dict | None:
    """

    :return:
    """
    url = 'https://labs.j-novel.club/app/v1/events'
    params = {
        'sort': 'launch',
        'start_date': datetime.utcnow().strftime(DATE_FORMAT),
        'limit': 600,
        'format': 'json'
    }

    logger.debug('Querying J-Novel Club new releases')
    response = requests.get(url, params=params)
    logger.debug(f'GET {url} - response status code: {response.status_code}')
    logger.debug(f'params: {params}')

    if response.status_code != 200:
        logger.error('Could not get information from J-Novel Club. Please check https://j-novel.club/calendar')
        return

    return response.json()


def _parse_new_releases(response: dict) -> list:
    """
    TODO
    :param response:
    :return:
    """
    result = []

    for release in response['events']:
        if release['details'] == 'Ebook Publishing' and release['serie']['type'] == 'NOVEL':
            new_release = {
                'date': datetime.strptime(release['launch'], DATE_FORMAT).strftime('%Y-%m-%d'),
                'name': release['name'],
                'serie': release['serie']['title'],
                'source': 'J-Novel Club'
            }
            result.append(new_release)

    if len(result) == 0:
        logger.error('Empty new release list')

    return result


def new_releases():
    """
    TODO
    :return:
    """
    logger.info('Fetching data from J-Novel Club')
    result = _get_new_releases()
    logger.info('Fetched all required data from J-Novel Club')
    return _parse_new_releases(result)
