import requests


def convert_cookies_to_dictionary(cookies: list):
    return {cookie["name"]: cookie["value"] for cookie in cookies}


def add_selenium_cookies_to_requests_session(
    session: requests.Session, selenium_cookies: dict
):
    for cookie_key, cookie_value in selenium_cookies.items():
        session.cookies.set(cookie_key, cookie_value)
    return
