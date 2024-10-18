import gzip
import requests
import brotli

from io import BytesIO

from sos.constants import TURNOUT_URL


def fetch_data(url):
    headers: dict[str, str] = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.5",
        "Accept-Encoding": "gzip, deflate, br",
        "Connection": "keep-alive",
        "Upgrade-Insecure-Requests": "1",
        "Referer": "https://sos.ga.gov/",
    }

    response = requests.get(url, headers=headers, timeout=10)

    # Read the response
    data = response.content

    content_encoding = response.headers.get("Content-Encoding")

    # Decompress if the content is gzip-encoded
    if content_encoding == "br":
        data = brotli.decompress(data)

    return data


def main():
    data = fetch_data(TURNOUT_URL)
    print(data)


if __name__ == "__main__":
    main()
