import gzip
import http.client
import ssl
from io import BytesIO
from urllib.parse import urlsplit

from .constants import TURNOUT_URL


def fetch_data(url):
    # Parse the URL
    parsed_url = urlsplit(url)
    host = parsed_url.hostname
    path = parsed_url.path

    # Create a connection
    context = ssl.create_default_context()
    connection = http.client.HTTPSConnection(host, context=context)

    # Make the request
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.5",
        "Accept-Encoding": "gzip, deflate, br",
        "Connection": "keep-alive",
        "Upgrade-Insecure-Requests": "1",
        "Referer": "https://sos.ga.gov/",
    }
    connection.request("GET", path, headers=headers)
    response = connection.getresponse()

    # Read the response
    data = response.read()

    content_encoding = response.getheader("Content-Encoding")

    # Decompress if the content is gzip-encoded
    if content_encoding == "gzip":
        buf = BytesIO(data)
        with gzip.GzipFile(fileobj=buf) as f:
            data = f.read()

    if response.status != 200:
        raise Exception(f"Failed to fetch data: {response.status} {response.reason}")

    connection.close()

    return data


def main():
    data = fetch_data(TURNOUT_URL)
    decoded_data = data.decode("utf-8")
    print(decoded_data)


if __name__ == "__main__":
    main()
