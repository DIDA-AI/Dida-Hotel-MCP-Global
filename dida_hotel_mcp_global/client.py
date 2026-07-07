import logging
from typing import Any, Dict, Optional

import httpx

from .config import API_BASE_URL

logger = logging.getLogger(__name__)

_client: Optional[httpx.AsyncClient] = None


def _get_client() -> httpx.AsyncClient:
    """Return a process-wide shared client so connections are pooled across requests."""
    global _client
    if _client is None or _client.is_closed:
        _client = httpx.AsyncClient(timeout=30.0, follow_redirects=True)
    return _client


async def request_api(method: str, endpoint: str, api_key: str, payload: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    url = f"{API_BASE_URL}{endpoint}"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Accept": "application/json",
    }
    if method.upper() == "POST":
        headers["Content-Type"] = "application/json"

    client = _get_client()
    try:
        response = await client.request(method.upper(), url, json=payload, headers=headers)
        response.raise_for_status()
        return response.json()
    except httpx.HTTPStatusError as e:
        # Log the full upstream body server-side; surface only the status to the caller
        # so internal backend details are not leaked to the MCP client.
        body = ""
        try:
            body = e.response.text
        except Exception:
            pass
        logger.warning("Upstream %s %s failed: status=%s body=%s", method, url, e.response.status_code, body)
        raise Exception(f"HTTP request failed (status {e.response.status_code})") from e
    except httpx.HTTPError as e:
        logger.warning("Upstream %s %s failed: %s", method, url, e)
        raise Exception(f"HTTP request failed: {str(e)}") from e
