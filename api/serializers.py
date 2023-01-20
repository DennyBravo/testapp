from api.models import Page, Link
from rest_framework import serializers


class LinkSerializer(serializers.ModelSerializer):
    linked_page = serializers.SlugRelatedField(
        many=False, read_only=True, slug_field="url"
    )

    class Meta:
        model = Link
        fields = ["linked_page", "anchor", "is_internal", "is_page_anchor"]
