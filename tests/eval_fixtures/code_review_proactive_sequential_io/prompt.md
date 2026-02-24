Write a Python async function `fetch_user_dashboard(user_id: int)` that:
1. Fetches user profile from GET /api/users/{user_id}
2. Fetches recent orders from GET /api/users/{user_id}/orders
3. Fetches notification count from GET /api/users/{user_id}/notifications/count

Use httpx as the HTTP client. Return a dict with keys: profile, orders, notification_count.
