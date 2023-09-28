from logging import getLogger
from os import path

from selenium.webdriver import Firefox
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.firefox.options import Options as FirefoxOptions

from webdriver_manager.firefox import GeckoDriverManager


logger = getLogger(__name__)


def init_driver(
        headless: bool = True,
        implicit_wait_time: int = 5
) -> Firefox:
    """
    Init the Selenium driver
    :param headless: TODO
    :param implicit_wait_time: TODO
    :return:
    """
    logger.info('Initializing selenium driver')
    logger.debug(f'headless mode: {headless}')

    firefox_options = FirefoxOptions()
    firefox_options.add_argument("-profile")
    firefox_options.add_argument("./profiles/firefox.selenium")
    if headless:
        firefox_options.add_argument('--headless')

    try:
        driver = Firefox(
            service=FirefoxService(
                GeckoDriverManager().install(), log_output=path.devnull
            ),
            options=firefox_options
        )
    except ValueError:
        logger.error('Error while using selenium installer, skipping install process')
        driver = Firefox(options=firefox_options)

    driver.implicitly_wait(implicit_wait_time)
    return driver


def close_driver(driver: Firefox):
    """
    Close the selenium driver
    :param driver: TODO
    """
    logger.info('Closing selenium driver')
    driver.quit()
