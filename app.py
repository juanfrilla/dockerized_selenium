from flask import Flask, request, jsonify, Response

from cloudflare_handler import CloudFlareSolver


app = Flask(__name__)


@app.route("/download_pdf", methods=["POST"])
def download_pdf():
    if not request.is_json:
        return jsonify({"error": "Request content-type must be application/json"}), 400

    entry_data = request.get_json()

    if not entry_data:
        return jsonify({"error": "No data provided"}), 400
    if "flaresolverr_data" not in entry_data:
        return jsonify({"error": "'flaresolverr_data' field is missing"}), 400
    
    data = entry_data.get("flaresolverr_data")
    
    response = CloudFlareSolver.obtain_pdf_response(data)

    if response is None:
        return jsonify({"error": "Failed to obtain response from CloudFlareSolver"}), 500


    return Response(response.content, content_type=response.headers["Content-Type"])


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3333)
