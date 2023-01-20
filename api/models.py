from datetime import datetime
from django.db import models


class Page(models.Model):
    url = models.CharField(max_length=1000, unique=True)
    parsed_on = models.DateTimeField(default=None, null=True)

    def __str__(self) -> str:
        return "{} ({})".format(self.url, self.parsed_on)

    def should_be_updated(self, page_last_updated: datetime) -> bool:
        return (self.parsed_on is None) or page_last_updated > self.parsed_on


class Link(models.Model):
    page = models.ForeignKey(Page, on_delete=models.CASCADE)
    linked_page = models.ForeignKey(
        Page, on_delete=models.DO_NOTHING, related_name="linked"
    )
    anchor = models.CharField(default=None, null=True, max_length=1000)
    is_internal = models.BooleanField(default=False)
    is_page_anchor = models.BooleanField(default=False)

    def __str__(self) -> str:
        return "{} => {} ({}, {})".format(
            self.page.url, self.linked_page.url, self.anchor, self.is_internal
        )
