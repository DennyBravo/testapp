from urllib.parse import ParseResult


def get_root_url(url_parts: ParseResult):
    return '{}://{}'.format(url_parts.scheme, url_parts.netloc)


def get_url_no_anchor(url_parts: ParseResult):
    root_url = get_root_url(url_parts)
    url = '{}{}'.format(root_url, url_parts.path)

    if url_parts.query != '':
        return '{}?{}'.format(url, url_parts.query)

    return url