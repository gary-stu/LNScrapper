"""
TODO
"""
import shutil
from argparse import ArgumentParser, Namespace
from logging import getLogger, Formatter, StreamHandler, DEBUG, INFO
from subprocess import Popen
from time import sleep

from tools import init_driver, close_driver, format_result, verify_list_format, save_list_as_csv
from sources import jnovel_club_new_releases, yenpress_new_releases, \
    seven_seas_new_releases, crossinfworld_new_releases, kodansha_new_releases


logger = getLogger('LNScrapper')


def main(_args: Namespace):
    """
    TODO
    :param _args:
    :return:
    """

    # Setting up loggers
    loggers = [
        'LNScrapper',
        'tools.browser',
        'tools.misc',
        'sources.yenpress',
        'sources.seven_seas',
        'sources.jnovel_club',
        'sources.crossinfworld',
        'sources.kodansha',
    ]
    formatter = Formatter('%(name)-21s | %(levelname)-8s | %(message)s')
    stream_handler = StreamHandler()
    stream_handler.setFormatter(formatter)

    for logger_name in loggers:
        # Set up logger
        _logger = getLogger(logger_name)
        _logger.addHandler(stream_handler)
        if _args.verbose:
            _logger.setLevel(DEBUG)
        else:
            _logger.setLevel(INFO)
        _logger.propagate = False

    logger.debug(f'loggers initialized')

    logger.info('Start')
    if _args.new_profile:
        logger.info('We will generate a "firefox.selenium" profile in the "./profiles" folder and open a new browser')
        logger.info('If you have never actively set a profile as default, it may switch the default profile.')
        logger.info('If needed, to restore the previous profile, please go to about:profiles on Firefox')

        logger.debug('Creating the new profile')
        process = Popen('firefox -profile "firefox.selenium ."')
        sleep(3)
        process.kill()
        sleep(3)
        logger.debug('Moving new profile in "profiles" folder')
        shutil.move('firefox.selenium', 'profiles')
        exit(0)

    if _args.challenge:
        logger.info('We will open the correct firefox profile.')
        logger.info('All required webpages will be opened in a tab. Please check every tab to validate access')

        urls = [
            'https://yenpress.com/calendar',
            'https://sevenseasentertainment.com/release-dates/'
        ]
        cmd_skel = [
            'firefox', '-profile', './profiles/firefox.selenium', '-new-tab'
        ]
        for url in urls:
            cmd = cmd_skel.copy()
            cmd.append(url)
            Popen(cmd)
        exit(0)

    driver = init_driver(headless=not _args.verbose)

    releases = []
    # sources not needing selenium
    releases.extend(jnovel_club_new_releases())
    releases.extend(crossinfworld_new_releases())
    releases.extend(kodansha_new_releases())

    # sources needing selenium
    releases.extend(yenpress_new_releases(driver))
    releases.extend(seven_seas_new_releases(driver))

    close_driver(driver)

    assert verify_list_format(releases)
    releases = format_result(releases)
    save_list_as_csv(releases)


# Setting up arg parser
parser = ArgumentParser('Scrapper for upcoming light novel releases')

parser.add_argument(
    '-n', '--new-profile',
    help='Generate a new firefox profile',
    action='store_true',
    dest='new_profile'
)

parser.add_argument(
    '-c', '--challenge',
    help='Start firefox with generated profile and open the webpages that might require a challenge',
    action='store_true',
    dest='challenge'
)

parser.add_argument(
    '-v', '--verbpse',
    help='Run is verbose mode: print debug logs',
    action='store_true',
    dest='verbose'
)

args = parser.parse_args()
main(args)
