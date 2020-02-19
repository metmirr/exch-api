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

    cheapest = CurrencyRate.get_cheapest_rate(code)
    if cheapest is None:
        return JsonResponse(
            {"error": "Currency code could not found"}, status=404
        )
    return JsonResponse(cheapest, safe=False)


def best_available_rate(request):
    code = request.GET.get("code")
    if code is None:
        return JsonResponse(
            {"error": "Please provide a currency code"}, status=400
        )
    code = code.lower()
    bar = CurrencyRate.get_best_available_rate(code)
    if bar is None:
        return JsonResponse(
            {"error": "Currency code could not found"}, status=404
        )
    return JsonResponse(bar, safe=False)
