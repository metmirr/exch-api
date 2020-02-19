from django.http import JsonResponse
from django.core.cache import cache

from .models import CurrencyRate


def rate(request):
    code = request.GET.get("code")
    if code is None:
        return JsonResponse(
            {"error": "Please provide a currency code"}, status=400
        )
    code = code.lower()

    from_cache = cache.get(code)
    if from_cache is not None:
        return JsonResponse(from_cache, safe=False)

    cheapest = CurrencyRate.get_rates(code)
    if cheapest is None:
        return JsonResponse(
            {"error": "Currency code could not found"}, status=404
        )
    return JsonResponse(cheapest, safe=False)


    cheapest = min(rates)
    cache.set(code, cheapest, 10)
    return JsonResponse(cheapest, safe=False)
