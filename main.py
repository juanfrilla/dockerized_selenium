import requests
from selenium_driverless.sync import webdriver
from flask import Flask, send_file, request, jsonify

from utils import (
    convert_cookies_to_dictionary,
    add_selenium_cookies_to_requests_session,
)


app = Flask(__name__)


@app.route("/download_pdf", methods=["POST"])
def download_pdf():
    session = requests.Session()
    data = request.get_json()
    if not data or "pdf_url" not in data:
        return jsonify({"error": "PDF URL not provided"}), 400

    pdf_url = data["pdf_url"]
    options = webdriver.ChromeOptions()
    options.add_argument("--headless=new")
    with webdriver.Chrome(options=options) as driver:
        driver.get(pdf_url)
        driver.sleep(2)
        cookies = driver.get_cookies()
        headers = {"User-Agent": driver.execute_script("return navigator.userAgent;")}

        add_selenium_cookies_to_requests_session(
            session, convert_cookies_to_dictionary(cookies)
        )
        response = session.get(pdf_url, headers=headers)

        return jsonify({"pdf_content": response.content})


if __name__ == "__main__":
    app.run(debug=True)
