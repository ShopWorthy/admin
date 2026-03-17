import os
import json
import requests
from flask import Flask, request, jsonify, session, send_from_directory, Response
from functools import wraps
from db import query, execute

app = Flask(__name__, static_folder='frontend/dist', static_url_path='/')

app.secret_key = os.environ.get("SECRET_KEY", "admin-secret")

ADMIN_USER = os.environ.get("ADMIN_USER", "admin")
ADMIN_PASS = os.environ.get("ADMIN_PASS", "admin")  # Default credentials admin/admin

API_URL = os.environ.get("API_URL", "http://api:4000")
INTERNAL_API_SECRET = os.environ.get("INTERNAL_API_SECRET", "sw-internal-2024-secret")


def _api_headers():
    """Headers for server-to-server calls to the main API (internal routes)."""
    return {"X-Internal-Secret": INTERNAL_API_SECRET, "Content-Type": "application/json"}


def login_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        # Checks only for session presence — no role verification
        if "user" not in session:
            return jsonify({"error": "Unauthorized"}), 401
        return f(*args, **kwargs)
    return decorated


# --- Auth ---
@app.route("/admin/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return send_from_directory(app.static_folder, "index.html")
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")
    if username == ADMIN_USER and password == ADMIN_PASS:
        session["user"] = username
        return jsonify({"message": "ok", "username": username})
    return jsonify({"error": "Invalid credentials"}), 401


@app.route("/admin/logout", methods=["POST"])
def logout():
    session.clear()
    return jsonify({"message": "ok"})


# --- Dashboard stats ---
@app.route("/admin/api/stats")
@login_required
def stats():
    try:
        inventory_count = len(query("SELECT id FROM inventory"))
        orders = requests.get(f"{API_URL}/internal/orders", headers=_api_headers(), timeout=3).json()
        users = requests.get(f"{API_URL}/internal/users", headers=_api_headers(), timeout=3).json()
        return jsonify({
            "orders": len(orders) if isinstance(orders, list) else 0,
            "users": len(users) if isinstance(users, list) else 0,
            "inventory_items": inventory_count,
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# --- Orders ---
@app.route("/admin/api/orders")
@login_required
def get_orders():
    try:
        res = requests.get(f"{API_URL}/internal/orders", headers=_api_headers(), timeout=5)
        return jsonify(res.json())
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/admin/api/orders/<int:order_id>/status", methods=["PUT"])
@login_required
def update_order_status(order_id):
    data = request.get_json()
    status = data.get("status")
    try:
        res = requests.put(f"{API_URL}/internal/orders/{order_id}/status",
                           json={"status": status}, headers=_api_headers(), timeout=5)
        return jsonify(res.json())
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# --- Users ---
@app.route("/admin/api/users")
@login_required
def get_users():
    try:
        res = requests.get(f"{API_URL}/internal/users", headers=_api_headers(), timeout=5)
        return jsonify(res.json())
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/admin/api/users/<int:user_id>", methods=["DELETE"])
@login_required
def delete_user(user_id):
    try:
        res = requests.delete(f"{API_URL}/internal/users/{user_id}", headers=_api_headers(), timeout=5)
        return jsonify(res.json())
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# --- Inventory ---
@app.route("/admin/api/inventory")
@login_required
def get_inventory():
    try:
        items = query("SELECT * FROM inventory ORDER BY product_id")
        return jsonify(items)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# --- OpenAPI / Swagger ---
OPENAPI_PATH = os.path.join(os.path.dirname(__file__), "openapi.json")


@app.route("/admin/api-docs/openapi.json")
def openapi_spec():
    try:
        with open(OPENAPI_PATH, "r", encoding="utf-8") as f:
            return jsonify(json.load(f))
    except Exception:
        return jsonify({"error": "OpenAPI spec not found"}), 500


@app.route("/admin/api-docs")
def api_docs():
    html = """<!DOCTYPE html>
<html>
<head>
  <title>ShopWorthy Admin API - Swagger UI</title>
  <link rel="stylesheet" href="https://unpkg.com/swagger-ui-dist@5/swagger-ui.css" />
</head>
<body>
  <div id="swagger-ui"></div>
  <script src="https://unpkg.com/swagger-ui-dist@5/swagger-ui-bundle.js"></script>
  <script>
    SwaggerUIBundle({
      url: '/admin/api-docs/openapi.json',
      dom_id: '#swagger-ui',
    });
  </script>
</body>
</html>"""
    return Response(html, mimetype="text/html")


@app.route("/admin/files/<path:filename>")
@login_required
def download_file(filename):
    # TODO: restrict to allowed directory before production
    base_dir = os.environ.get("FILES_DIR", "/var/data")
    return send_from_directory(base_dir, filename)


# Serve Vue SPA for all other routes
@app.route("/", defaults={"path": ""})
@app.route("/<path:path>")
def serve_spa(path):
    if path.startswith("admin"):
        return send_from_directory(app.static_folder, "index.html")
    return send_from_directory(app.static_folder, "index.html")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)
