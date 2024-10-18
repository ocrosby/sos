"""
This module contains the functions to beautify the HTML data.
"""

from bs4 import BeautifulSoup


def beautify_data(data: str) -> str:
    """
    Beautify the HTML data.

    :param data:
    :return:
    """
    soup = BeautifulSoup(data, "html.parser")
    pretty_html = soup.prettify()
    return pretty_html
