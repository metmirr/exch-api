import requests
from django.core.cache import cache
from django.conf import settings


class CurrencyRate(object):
    FOR_ONE_DAY = 60 * 60 * 24

    @classmethod
    def set_best_available_rate(cls, code, value):
        """Set best available rate for 24 hour."""

        bar_cache_lookup_key = code + "_bar"  # Best available rate (BAR)
        best_available_rate = cache.get(bar_cache_lookup_key)

        if best_available_rate is not None and best_available_rate > value:
            cache.set(bar_cache_lookup_key, value, cls.FOR_ONE_DAY)
        else:
            cache.set(bar_cache_lookup_key, value, cls.FOR_ONE_DAY)

    @classmethod
    def get_cheapest_rate(cls, code):
        """Returns cheapest rate for the given currency code"""

        rates = []
        for provider in settings.PROVIDERS:
            resp = requests.get(provider["url"])

            code_lookup_key = provider["code"]
            rate_lookup_key = provider["rate"]

            for d in resp.json():
                if d[code_lookup_key] == code:
                    rates.append(d[rate_lookup_key])

        if not rates:
            return None

        cheapest = min(rates)
        cache.set(code, cheapest, 60 * 10)

        cls.set_best_available_rate(code, cheapest)
        return cheapest

    @classmethod
    def get_best_available_rate(cls, code):
        """Returns best available rate for the given currency code"""

        bar_cache_lookup_key = code + "_bar"  # Best available rate (BAR)
        best_available_rate = cache.get(bar_cache_lookup_key)

        if best_available_rate is None:
            return cls.get_cheapest_rate(code)
        return best_available_rate
