from django.core import serializers
from django.http import HttpResponse, JsonResponse
from rest_framework.generics import ListAPIView
from django.views.decorators.csrf import csrf_exempt
from api.core.crawl import process_url
from api.serializers import LinkSerializer


@csrf_exempt
def parse(request):
    if request.method == 'POST':
        page_url = request.POST['url']
        links = process_url(page_url)
        serializer = LinkSerializer(links, many=True)
        return JsonResponse(serializer.data, safe=False)

    return HttpResponse('Method not supported')
