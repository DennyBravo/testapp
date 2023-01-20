from django.test import TestCase
from django.template.loader import render_to_string

from api.core.crawl import get_links_from_html


class CrawlerCase(TestCase):
    def test_nested_links(self):
        html = render_to_string("crawler/test.html")

        links = get_links_from_html(html)

        print(links)
        self.assertEqual(len(links), 6)
