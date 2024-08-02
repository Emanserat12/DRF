import uuid

import pytest
from rest_framework.test import APIClient

from myApp.models import Products


@pytest.fixture()
def api_client() -> APIClient:
    yield APIClient()


@pytest.fixture()
def fetch_list_of_products(api_client):
    products = Products.objects.all(is_removed=False)
    return products


@pytest.fixture()
def unique_product_payload():
    unique_str = str(uuid.uuid4())[:8]
    return {
        'name': f"Product_{unique_str}",
        'price': 5.78,
        'description': f"Description_{unique_str}",
        'category': f"Category_{unique_str}",
    }


@pytest.fixture()
def create_product():
    unique_str = str(uuid.uuid4())[:8]  # Generate a short unique string
    product_payload = {
        'name': f"Product_{unique_str}",
        'price': 8.78,
        'description': f"Description_{unique_str}",
        'category': f"Category_{unique_str}",
    }
    product = Products.objects.create(**product_payload)
    return product, product_payload
