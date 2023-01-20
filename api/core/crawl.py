from pytz import utc
import requests
from datetime import datetime
from bs4 import BeautifulSoup, Tag
from urllib.parse import urlparse
from api.core.parse import parse_tag
from api.core.url import get_root_url, get_url_no_anchor
from api.models import Page, Link


def get_last_modified_stamp(url: str):
    req = requests.head(url)
    last_modified_str = req.headers['last-modified']

    if (last_modified_str is None):
        last_modified = None
    else:
        last_modified = datetime.strptime(
            last_modified_str, '%a, %d %b %Y %H:%M:%S %Z')
        last_modified = last_modified.replace(tzinfo=utc)

    return last_modified


def process_link(root_url: str, url_no_anchor: str, href: str, page: Page) -> dict:
    is_internal = False
    full_link = href
    is_target_page_anchor = False

    if href is None:
        return
    elif href.startswith('#'):
        is_target_page_anchor = True
        is_internal = True
        full_link = '{}{}'.format(url_no_anchor, href)
    elif href.startswith('/') and not href.startswith('//'):
        is_internal = True
        full_link = '{}{}'.format(root_url, href)

    [linked_page, _] = Page.objects.get_or_create(
        url=(url_no_anchor if is_target_page_anchor else full_link),
        defaults=dict(url=full_link)
    )

    Link.objects.update_or_create(
        page=page,
        linked_page=linked_page,
        anchor=(href if is_target_page_anchor else None),
        is_internal=is_internal,
        is_page_anchor=is_target_page_anchor
    )


def potential_link_holder(tag: Tag):
    return \
        tag.name == 'a' or \
        tag.attrs.get('onclick') is not None


def get_links_from_html(html: str):
    soup = BeautifulSoup(html, 'html.parser')
    link_holders = soup.find_all(potential_link_holder)
    links = []

    for item in link_holders:
        link = parse_tag(item)
        links.append(link)

    return links


def parse_page_data(url: str, page: Page):
    url_parts = urlparse(url)
    root_url = get_root_url(url_parts)
    url_no_anchor = get_url_no_anchor(url_parts)
    html_text = requests.get(url).text
    links = get_links_from_html(html_text)

    for link in links:
        process_link(root_url, url_no_anchor, link, page)


def process_url(page_url: str):
    [page, _] = Page.objects.get_or_create(
        url=page_url,
        defaults=dict(url=page_url)
    )

    last_modified = get_last_modified_stamp(page_url)
    should_update = page.should_be_updated(last_modified)

    if (should_update):
        parse_page_data(page_url, page)
        page.parsed_on = datetime.now()
        page.save()

    links = Link.objects.filter(page=page)

    return links
