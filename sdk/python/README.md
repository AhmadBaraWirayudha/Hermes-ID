# Python SDK

A lightweight Python client for the IndoMarket Insight FastAPI service.

Example:

```python
from indomarket_client import IndoMarketClient

client = IndoMarketClient("http://localhost/api", token="change-me")
print(client.health())
print(client.summary())
```
