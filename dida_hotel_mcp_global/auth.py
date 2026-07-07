from fastmcp.server.dependencies import get_http_request


def extract_api_key() -> str:
    api_key = ""
    try:
        request = get_http_request()
        if request:
            headers = request.headers
            auth_header = (
                headers.get("authorization")
                or headers.get("Authorization")
                or headers.get("x-secret-key")
                or headers.get("X-Secret-Key")
                or ""
            )
            if auth_header:
                # Auth scheme is case-insensitive per RFC 7235; accept bearer/BEARER/etc.
                if auth_header[:7].lower() == "bearer ":
                    api_key = auth_header[7:].strip()
                else:
                    api_key = auth_header.strip()
    except RuntimeError:
        # Outside an HTTP context, get_http_request() raises RuntimeError
        pass

    if not api_key:
        raise Exception("No API Key provided. Add `Authorization: Bearer <your_api_key>` to the request header.")

    return api_key
