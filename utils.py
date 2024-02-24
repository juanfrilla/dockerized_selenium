import requests
from botasaurus import *
from botasaurus.create_stealth_driver import create_stealth_driver


def convert_cookies_to_dictionary(cookies: list):
    return {cookie["name"]: cookie["value"] for cookie in cookies}


def add_selenium_cookies_to_requests_session(
    session: requests.Session, selenium_cookies: dict
):
    for cookie_key, cookie_value in selenium_cookies.items():
        session.cookies.set(cookie_key, cookie_value)
    return


def get_start_url(data):
    return data


@browser(
    # user_agent=bt.UserAgent.REAL,
    # window_size=bt.WindowSize.REAL,
    max_retry=100,
    headless=True,
    create_error_logs=False,
    block_resources=True,
    close_on_crash=True,
    is_eager=True,
    create_driver=create_stealth_driver(
        start_url=get_start_url,
        raise_exception=True,
    ),
)
def get_requests_dict(driver: AntiDetectDriver, data):
    cookies = driver.get_cookies()
    user_agent = driver.execute_script("return navigator.userAgent;")
    return {
        "cookies": cookies,
        "user_agent": user_agent,
    }
