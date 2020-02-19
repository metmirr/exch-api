import requests
from django.core.cache import cache
from django.conf import settings


class CurrencyRate(object):

    BAR = None  # Best available rate

    @classmethod
    def get_rates(cls, code):
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

        if cls.BAR is not None and cls.BAR > cheapest:
            cls.BAR = cheapest

        return cheapest
