import requests
from flask import Flask, request, jsonify, Response

from utils import (
    convert_cookies_to_dictionary,
    add_selenium_cookies_to_requests_session,
    get_requests_dict,
)


app = Flask(__name__)


@app.route("/download_pdf", methods=["POST"])
def download_pdf():
    session = requests.Session()
    data = request.get_json()
    if not data or "pdf_url" not in data:
        return jsonify({"error": "PDF URL not provided"}), 400

    pdf_url = data["pdf_url"]
    requests_dict = get_requests_dict([pdf_url])[0]
    cookies = requests_dict["cookies"]
    headers = {"User-Agent": requests_dict["user_agent"]}

    add_selenium_cookies_to_requests_session(
        session, convert_cookies_to_dictionary(cookies)
    )
    response = session.get(pdf_url, headers=headers)
    return Response(response.content, content_type=response.headers["Content-Type"])


if __name__ == "__main__":
    app.run(debug=True)
