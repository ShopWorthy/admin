# admin

**Admin panel** for ShopWorthy — Vue 3 frontend + Python Flask backend. Manages orders, users, and inventory; shares PostgreSQL with the inventory service.

Part of the [ShopWorthy](https://github.com/ShopWorthy) organization.

## Technology

| Layer | Choice |
|-------|--------|
| Frontend | Vue 3 (Composition API) + Vite |
| Backend | Python Flask |
| Database | PostgreSQL (shared with inventory) |
| Auth | Session-based (Flask sessions) |
| Styling | Bootstrap 5 |

## Prerequisites

- Node.js 20+ (for frontend build)
- Python 3.11+ (for backend)
- npm or yarn, pip

## Setup

**Backend:**

```bash
cd backend
pip install -r requirements.txt
```

**Frontend:**

```bash
cd frontend
npm install
```

## Run (development)

**Option A — backend only (serves built frontend):**  
Build frontend once, then run Flask:

```bash
cd frontend && npm run build && cd ..
cd backend && python app.py
```

**Option B — dev with hot reload:**  
Terminal 1 (backend): `cd backend && python app.py`  
Terminal 2 (frontend): `cd frontend && npm run dev`

The admin panel will be available at **http://localhost:8080** (Flask) or **http://localhost:8081** (Vue dev server when used).

## Default credentials

| Username | Password |
|----------|----------|
| admin | admin |

## Docker

```bash
docker build -t shopworthy-admin .
docker run -p 8080:8080 shopworthy-admin
```

## Port

| Environment | Port |
|-------------|------|
| Flask (production) | 8080 |
| Vue dev server | 8081 |

## Related Repositories

- [inventory](https://github.com/ShopWorthy/inventory) — Shares PostgreSQL with this service
- [api](https://github.com/ShopWorthy/api) — Primary API (orders/users data)
- [infra](https://github.com/ShopWorthy/infra) — Full stack via Docker Compose
