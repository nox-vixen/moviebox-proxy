import httpx
import hashlib
import hmac
import base64
import time
import json

HOST = "https://h5-api.aoneroom.com"

SECRET_KEY = "76iRl07s0xSN9jqmEWAt79EBJZulIQIsV64FZr2O"


def md5_hex(data):
    return hashlib.md5(data).hexdigest()


def x_client_token():
    ts = str(int(time.time() * 1000))
    return f"{ts},{md5_hex(ts[::-1].encode())}"


def b64decode(s):
    padding = (4 - len(s) % 4) % 4
    return base64.b64decode(s + "=" * padding)


def sign(method, url):
    ts = int(time.time() * 1000)

    canonical = (
        f"{method}\n"
        "application/json\n"
        "application/json\n\n"
        f"{ts}\n\n"
        f"{url}"
    )

    secret = b64decode(SECRET_KEY)

    sig = hmac.new(
        secret,
        canonical.encode(),
        hashlib.md5
    ).digest()

    sig = base64.b64encode(sig).decode()

    return f"{ts}|2|{sig}"


async def moviebox_get(path):
    url = HOST + path

    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
        "X-Client-Token": x_client_token(),
        "x-tr-signature": sign(
            "GET",
            url
        )
    }

    async with httpx.AsyncClient() as client:
        r = await client.get(
            url,
            headers=headers
        )

        return {
            "url": str(r.url),
            "status": r.status_code,
            "headers": dict(r.headers),
            "text": r.text
        }
