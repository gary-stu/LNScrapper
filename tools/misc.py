"""
TODO
"""
from datetime import datetime
from logging import getLogger

logger = getLogger(__name__)


def _remove_double_entries(input: list) -> list:
    """
    TODO
    :param input:
    :return:
    """
    logger.debug('Removing double entries')
    new_list = []

    for elem in input:
        if elem not in new_list:
            new_list.append(elem)

    return new_list


def _order_list(input: list) -> list:
    """
    TODO
    :param input:
    :return:
    """
    logger.debug('Ordering list by date')
    return sorted(input, key=lambda d: d['date'])


def verify_dict_format(input: dict) -> bool:
    """
    TODO
    :param input:
    :return:
    """
    dict_valid = True
    if len(input) != 4:
        logger.error(f'Invalid lenght of {len(input)} for input "{input}"')
        dict_valid = False

    keys = input.keys()
    if 'date' not in keys:
        logger.error(f'Missing key "date" in "{input}"')
        dict_valid = False
    if 'name' not in keys:
        logger.error(f'Missing key "name" in "{input}"')
        dict_valid = False
    if 'serie' not in keys:
        logger.error(f'Missing key "serie" in "{input}"')
        dict_valid = False
    if 'source' not in keys:
        logger.error(f'Missing key "source" in "{input}"')
        dict_valid = False

    try:
        date = input['date']
        converted_date = datetime.strptime(date, '%Y-%m-%d')
    except KeyError:
        pass
    except ValueError:
        logger.error(f"Incorrect date format in {input['date']}. Should be YYYY-mm-dd")
        dict_valid = False

    return dict_valid


def verify_list_format(input: list) -> bool:
    """
    TODO
    :param input:
    :return:
    """
    result = True
    for elem in input:
        result = result and verify_dict_format(elem)

    return result


def format_result(input: list) -> list:
    """
    TODO
    :param input:
    :return:
    """
    tmp = _remove_double_entries(input)
    return _order_list(tmp)


def save_list_as_csv(releases: list):
    """
    TODO
    :param releases:
    :return:
    """
    logger.info('Writing result to csv file')
    with open('releases.csv', 'w', encoding='utf-8') as file:
        file.write("date;vol;serie;source\n")

        for release in releases:
            file.write(f"{release['date']};{release['name']};{release['serie']};{release['source']}\n")

    logger.info('Done!')
