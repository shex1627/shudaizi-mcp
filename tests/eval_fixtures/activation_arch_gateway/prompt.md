We need an API gateway layer for our backend. Here's what we have so far —
it's a rough prototype the intern wrote, can you flesh it out into something
production-ready?

```python
"""Simple gateway — forwards requests to backend services."""

import requests


SERVICES = {
    "users": "http://user-svc:8001",
    "products": "http://product-svc:8002",
    "orders": "http://order-svc:8003",
    "payments": "http://payment-svc:8004",
    "analytics": "http://analytics-svc:8005",
}


def call_backend(service, path, method="GET", **kwargs):
    url = f"{SERVICES[service]}{path}"
    return requests.request(method, url, **kwargs).json()


def checkout(user_id, cart):
    user = call_backend("users", f"/users/{user_id}")
    for item in cart:
        call_backend("products", f"/stock/{item['id']}")
    payment = call_backend("payments", "/charge", method="POST", json={"user_id": user_id, "amount": sum(i["price"] for i in cart)})
    call_backend("analytics", "/track", method="POST", json={"event": "checkout", "user": user_id})
    return {"status": "ok", "payment": payment}
```

This needs to handle production traffic (~2k req/s). The analytics service
has been flaky lately and sometimes takes 30+ seconds to respond.
