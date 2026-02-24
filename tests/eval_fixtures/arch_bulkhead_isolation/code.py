"""API gateway that proxies requests to multiple backend services.

Routes checkout, product page, and dashboard requests to 6 backend services.
"""

from __future__ import annotations

import time
from concurrent.futures import ThreadPoolExecutor
from dataclasses import dataclass
from typing import Any

import requests


# ── Shared resources ─────────────────────────────────────────────

# Single thread pool shared by ALL backend calls
_executor = ThreadPoolExecutor(max_workers=10)

# Single HTTP session shared by ALL backend calls
_session = requests.Session()
_session.headers.update({"X-Gateway": "api-gw-01"})


# ── Backend service clients ──────────────────────────────────────


@dataclass
class ServiceConfig:
    name: str
    base_url: str


SERVICES = {
    "user": ServiceConfig("User Service", "http://user-service:8001"),
    "catalog": ServiceConfig("Catalog Service", "http://catalog-service:8002"),
    "payment": ServiceConfig("Payment Service", "http://payment-service:8003"),
    "inventory": ServiceConfig("Inventory Service", "http://inventory-service:8004"),
    "notification": ServiceConfig("Notification Service", "http://notification-service:8005"),
    "analytics": ServiceConfig("Analytics Service", "http://analytics-service:8006"),
}


def call_service(service_name: str, path: str, method: str = "GET", **kwargs) -> dict:
    """Make an HTTP call to a backend service using the shared pool and session."""
    config = SERVICES[service_name]
    url = f"{config.base_url}{path}"

    future = _executor.submit(_session.request, method, url, timeout=30, **kwargs)
    response = future.result()
    response.raise_for_status()
    return response.json()


# ── API endpoint handlers ────────────────────────────────────────


def handle_checkout(user_id: str, cart_items: list[dict]) -> dict:
    """Process a checkout — calls 4 backend services."""
    # All these calls go through the same thread pool and session
    user = call_service("user", f"/users/{user_id}")

    for item in cart_items:
        call_service("inventory", f"/check/{item['product_id']}")

    payment = call_service("payment", "/charge", method="POST", json={
        "user_id": user_id,
        "amount": sum(i["price"] * i["qty"] for i in cart_items),
    })

    call_service("notification", "/send", method="POST", json={
        "user_id": user_id,
        "type": "order_confirmation",
        "payment_id": payment["id"],
    })

    return {"status": "completed", "payment_id": payment["id"]}


def handle_product_page(product_id: str, user_id: str | None = None) -> dict:
    """Render a product page — calls 3 backend services."""
    product = call_service("catalog", f"/products/{product_id}")
    inventory = call_service("inventory", f"/stock/{product_id}")

    recommendations = call_service("analytics", f"/recommend/{product_id}")

    result = {**product, "stock": inventory["available"], "recommendations": recommendations}

    if user_id:
        user_prefs = call_service("user", f"/users/{user_id}/preferences")
        result["personalized"] = True

    return result


def handle_dashboard(user_id: str) -> dict:
    """User dashboard — calls 4 backend services."""
    user = call_service("user", f"/users/{user_id}")
    orders = call_service("payment", f"/orders/{user_id}")
    notifications = call_service("notification", f"/unread/{user_id}")
    activity = call_service("analytics", f"/activity/{user_id}")

    return {
        "user": user,
        "recent_orders": orders,
        "unread_notifications": notifications,
        "activity_summary": activity,
    }


def health_check() -> dict:
    """Check all backend services — if any hangs, blocks the shared pool."""
    results = {}
    for name in SERVICES:
        try:
            call_service(name, "/health")
            results[name] = "healthy"
        except Exception as e:
            results[name] = f"unhealthy: {e}"
    return results
