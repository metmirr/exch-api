from django.test import TestCase
from django.core.cache import cache
from django.conf import settings

from .models import CurrencyRate


class TestCurrencyRate(TestCase):
    def test_get_best_available_rate(self):
        bar = CurrencyRate.get_best_available_rate("usd")
        self.assertIsNotNone(bar)

        bar = CurrencyRate.get_best_available_rate("asd")
        self.assertIsNone(bar)

    def test_set_best_available_rate(self):
        rate, code = "4.24472", "usd"

        CurrencyRate.set_best_available_rate(code, rate)
        self.assertEqual(rate, CurrencyRate.get_best_available_rate(code))

    def test_get_best_available_rate_from_cache(self):
        bar = CurrencyRate.get_best_available_rate("usd")
        bar_from_cache = cache.get("usd_bar")
        self.assertEqual(bar, bar_from_cache)

    def test_get_cheapest_rate(self):
        cheapest = CurrencyRate.get_cheapest_rate("usd")
        self.assertIsNotNone(cheapest)

        cheapest = CurrencyRate.get_cheapest_rate("asdf")
        self.assertIsNone(cheapest)


class TestCurrencyRateAPI(TestCase):
    def test_get_cheapest_success(self):
        resp = self.client.get("/api/rate?code=GBP")
        self.assertEqual(200, resp.status_code)

    def test_get_cheapest_fail(self):
        resp = self.client.get("/api/rate?code=asd")
        error_msg = resp.json()["error"]

        self.assertEqual(404, resp.status_code)
        self.assertEqual(error_msg, "Currency code could not found")

    def test_best_available_rate(self):
        resp = self.client.get("/api/bar?code=USD")
        self.assertEqual(200, resp.status_code)


class TestProviders(TestCase):
    def test_providers(self):
        self.assertEqual(3, len(settings.PROVIDERS))

        settings.PROVIDERS.pop()
        self.assertEqual(2, len(settings.PROVIDERS))

        first_provider = settings.PROVIDERS[0]
        self.assertTrue(first_provider["url"])

