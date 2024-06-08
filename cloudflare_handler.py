import os
import json
import requests


class CloudFlareSolver(object):
    """
    FlareSolverr para vulnerar el clouflare, está conectado a un servicio que
    debe estar levantado (en docker, ~/modulos/docker/docker_flaresolverr)
    (Funciona en paralelo, varias instancias de esto)
    """

    @classmethod
    def convert_cookies_to_dictionary(cls, cookies: list):
        return {cookie["name"]: cookie["value"] for cookie in cookies}

    @classmethod
    def add_cookies_to_requests_session(cls, session: requests.Session, cookies: list):
        for cookie_key, cookie_value in cls.convert_cookies_to_dictionary(
            cookies
        ).items():
            session.cookies.set(cookie_key, cookie_value)
        return

    @classmethod
    def obtain_raw_response(
        cls,
        data: dict,
    ) -> dict:
        app_env = os.getenv('APP_ENV', 'local')
        api_url = "http://flaresolverr:8191/v1" if app_env == "docker" else "http://localhost:8191/v1"
        headers = {"Content-Type": "application/json"}

        response = requests.post(api_url, headers=headers, json=data)
        response_data = json.loads(response.content)
        return response_data
    
    @classmethod
    def obtain_pdf_response(cls, data: dict) -> requests.Response:
        proxy = data.get("proxy")
        raw_response = cls.obtain_raw_response(data)
        if raw_response.get("solution"):
            solution = raw_response.get("solution")
            cookies = solution.get("cookies")
            url_scrape = solution.get("url")
            user_agent = solution.get("userAgent")
            for cookie in cookies:
                if cookie["name"] == "cf_clearance":
                    session = requests.Session()
                    cls.add_cookies_to_requests_session(session, cookies)
                    
                    proxy = proxy.get('url').replace("https://", "") if proxy else None

                    response = session.get(url_scrape, headers={"user-agent": user_agent}, proxies = {"http": proxy, "https": proxy})
                    if response.status_code == 200 and type(response.content) == bytes and response.content != b"":
                        return response
        return None