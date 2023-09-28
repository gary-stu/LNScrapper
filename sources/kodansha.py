"""
TODO
"""
import requests
from datetime import datetime
from logging import getLogger

logger = getLogger(__name__)


def _get_api() -> dict | None:
    """
    TODO
    :return:
    """
    url = 'https://api.kodansha.us/product/ReleaseCalendar'
    params = {'filterBy': 'book'}
    logger.debug('Querying Kodansha new releases')
    response = requests.get(url, params=params)
    
    logger.debug(f'GET {url} - response status code: {response.status_code}')
    logger.debug(f'params: {params}')

    if response.status_code != 200:
        logger.error(f'Query response code: {response.status_code}')
        return

    return response.json()


def _find_novels(data: dict):
    """
    TODO
    :param data:
    :return:
    """
    releases = []

    for elem in data['digital']:
        name = elem['name']
        name = name.split(' (light novel)')[0]

        serie = name
        while serie[-1].isdigit() or serie[-1] == ' ':
            serie = serie.rstrip(serie[-1])

        date = datetime.strptime(elem['releaseDate'], '%m/%d/%Y').strftime('%Y-%m-%d')

        release = {
            'date': date,
            'name': name,
            'serie': serie,
            'source': 'Kodansha'
        }
        releases.append(release)

    return releases


def new_releases() -> list:
    """
    TODO
    :return:
    """
    logger.info('Fetching data from Kodansha')
    data = _get_api()
    if data is None:
        return []

    releases = _find_novels(data)
    logger.info('Fetched all required data from Kodansha')

    return releases
