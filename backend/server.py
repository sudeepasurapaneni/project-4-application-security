import os
from urllib.parse import urlparse

import requests
from dotenv import load_dotenv
from flask import Flask, jsonify, request
from flask_cors import CORS

load_dotenv()
app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "*"}})

SECURITY_HEADERS = [
    "Content-Security-Policy",
    "Strict-Transport-Security",
    "X-Content-Type-Options",
    "X-Frame-Options",
    "Referrer-Policy",
]


@app.get("/api/")
def health_check():
    return jsonify({"message": "WebGuard API is ready"})


@app.post("/api/scan")
def scan_website():
    payload = request.get_json(silent=True) or {}
    target_url = str(payload.get("url", "")).strip()
    parsed = urlparse(target_url)
    if parsed.scheme not in {"http", "https"} or not parsed.netloc:
        return jsonify({"error": "Please enter a valid HTTP or HTTPS URL."}), 400

    ssl_warning = None
    try:
        response = requests.get(
            target_url, timeout=15, allow_redirects=True,
            headers={"User-Agent": "Mozilla/5.0 (WebGuard security scanner)"},
            verify=True,
        )
    except requests.Timeout:
        return jsonify({"error": "Request timed out after 15 seconds."}), 422
    except requests.exceptions.SSLError as error:
        reason = str(error)
        if "certificate has expired" in reason.lower():
            try:
                response = requests.get(
                    target_url, timeout=15, allow_redirects=True,
                    headers={"User-Agent": "Mozilla/5.0 (WebGuard security scanner)"},
                    verify=False,
                )
                ssl_warning = (
                    "Warning: the SSL certificate is expired/untrusted. "
                    "Headers were inspected with certificate verification disabled; "
                    "the certificate is not considered valid."
                )
            except requests.Timeout:
                return jsonify({"error": "Request timed out after 15 seconds."}), 422
            except requests.RequestException as retry_error:
                retry_reason = str(retry_error).split(" (Caused by", 1)[0].strip()
                return jsonify({"error": f"Expired SSL fallback request failed: {retry_reason}"}), 422
        elif "certificate verify failed" in reason.lower():
            return jsonify({"error": "SSL certificate verification failed: certificate is untrusted."}), 422
        else:
            return jsonify({"error": f"SSL certificate verification failed: {reason}"}), 422
    except requests.RequestException as error:
        reason = str(error).split(" (Caused by", 1)[0].strip()
        return jsonify({"error": f"Request failed: {reason}"}), 422

    results = []
    for header in SECURITY_HEADERS:
        value = response.headers.get(header)
        results.append({"name": header, "present": bool(value), "value": value or None})

    return jsonify({
        "url": target_url, "final_url": response.url,
        "status_code": response.status_code,
        "response_headers": dict(response.headers), "headers": results,
        "issues_found": sum(1 for item in results if not item["present"]),
        "ssl_verified": ssl_warning is None, "ssl_warning": ssl_warning,
    })


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", "5000")), debug=False)
