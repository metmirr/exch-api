from collections import namedtuple

from django.conf import settings
from django.http import JsonResponse
import requests


def rate(request):
    code = request.GET.get("code")
    if code is None:
        return JsonResponse(
            {"error": "Please provide a currency code"}, status=400
        )
    code = code.lower()

    rates = []
    for provider in settings.PROVIDERS:
        resp = requests.get(provider["url"])

        code_lookup_key = provider["code"]
        rate_lookup_key = provider["rate"]

        for d in resp.json():
            if d[code_lookup_key] == code:
                rates.append(d[rate_lookup_key])
    if not rates:
        return JsonResponse(
            {"error": "Currency code could not found"}, status=404
        )

    return JsonResponse(min(rates), safe=False)
