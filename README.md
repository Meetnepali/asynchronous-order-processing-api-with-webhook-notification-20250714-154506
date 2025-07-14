# Asynchronous Order Processing API (FastAPI)

## Task Overview

Develop a FastAPI application that provides endpoints for placing and retrieving orders. Upon placing an order, validate the payload using Pydantic, persist it asynchronously to a relational database using SQLAlchemy Async, and asynchronously notify an external webhook endpoint (URL configurable via environment variable). Organize endpoints via routers and use DI for session management. Handle validation, database, and webhook errors gracefully. Robust request/response examples and error responses should be included in the OpenAPI schema.

#### Requirements:
- **POST /orders/**: Place a new order
    - Validate request with Pydantic
    - Save to database asynchronously
    - Trigger a background task notifying a configurable external webhook
- **GET /orders/{order_id}**: Retrieve an order by ID
- Use SQLAlchemy async with dependency injection for async session management
- Webhook URL should be set via environment variable
- All endpoints should be organized using FastAPI routers
- Implement robust error handling for input validation, db, and webhook notification
- Document the API with clear examples and error models (OpenAPI schema)

---

## Setup Instructions

1. **Clone the repository** (if not already present) and navigate to the project root.

2. **Environment variables:**
   - Copy `.env.example` to `.env` and update `WEBHOOK_URL` as needed, or export variables before startup.

3. **Verify your implementation:**
   - The service starts on [http://localhost:8000](http://localhost:8000)
   - Visit `/docs` for interactive API documentation and try placing/retrieving orders.
   - After placing an order, confirm webhook POST request is sent to the configured webhook URL.

---

## Notes
- You may use a test webhook URL such as https://webhook.site for manual verification.
- Ensure schema examples and error models appear as expected in the OpenAPI docs.
- All database migrations/initialization must be handled automatically at startup or via scripts.
- No need to implement authentication.
