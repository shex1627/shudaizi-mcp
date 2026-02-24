The product page is loading really slowly in production. Can you add a
`load_product_page(product_id: str, user_id: str)` function to this service?

It needs to grab the product details from the catalog service, check current
inventory level, and pull the user's purchase history for personalized
recommendations.

Here's the existing service code:

```python
"""Product service — handles product-related API calls."""

import requests

API_BASE = "http://internal-api:8000"
_session = requests.Session()


def get_product(product_id: str) -> dict:
    resp = _session.get(f"{API_BASE}/catalog/products/{product_id}", timeout=10)
    resp.raise_for_status()
    return resp.json()


def get_inventory(product_id: str) -> dict:
    resp = _session.get(f"{API_BASE}/inventory/{product_id}", timeout=10)
    resp.raise_for_status()
    return resp.json()


def get_user_history(user_id: str) -> list:
    resp = _session.get(f"{API_BASE}/users/{user_id}/purchases", timeout=10)
    resp.raise_for_status()
    return resp.json()
```

Follow the existing patterns in the codebase. Return a dict with keys:
product, inventory, recommendations.
