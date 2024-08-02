import uuid
from venv import logger

import pytest
from rest_framework import status

url = '/products/'


@pytest.mark.skip
def test_fetch_products(api_client):
    response = api_client.get(url)
    assert response.status_code == status.HTTP_200_OK
    assert response.data['message'] == 'Products Retrieved Successfully'


@pytest.mark.skip
def test_create_product(api_client, unique_product_payload):
    response = api_client.post(url, data=unique_product_payload, format='json')

    print(f"Status Code: {response.status_code}")
    print(f"Response Data: {response.data}")

    assert response.status_code == status.HTTP_201_CREATED
    assert response.data['message'] == 'Product Added Successfully'


@pytest.mark.skip
def test_create_product_with_invalid_price(api_client):
    unique_str = str(uuid.uuid4())[:8]
    invalid_product_payload = {
        'name': f"Product_{unique_str}",
        'price': "0.0",
        'description': f"Description_{unique_str}",
        'category': f"Category_{unique_str}",
    }
    response = api_client.post(url, data=invalid_product_payload, format='json')

    print(f"Status Code: {response.status_code}")
    print(f"Response Data: {response.data}")

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert 'price' in response.data
    assert response.data['price'][0] == 'Price has to be between 1.00 and 1000.00'


@pytest.mark.skip
def test_create_product_with_missing_fields(api_client):
    payload = {
        "name": "USB",
        "price": 10.0
    }
    response = api_client.post(url, data=payload, format='json')

    print(f"Status Code: {response.status_code}")
    print(f"Response Data: {response.data}")

    required_fields = ['name', 'price', 'description', 'category']

    missing_fields = [field for field in required_fields if field not in payload]
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    for field in missing_fields:
        assert field in response.data, f"Field '{field}' is missing from the response data"


@pytest.mark.skip
def test_update_product(api_client, create_product):
    url_ = f'/products/{create_product[0].id}/'
    payload = {
        "name": "Banknote counter updated"
    }
    response = api_client.patch(url_, data=payload, format='json')
    print(f'status code {response.status_code}')
    print(f'Response Data {response.data}')
    assert response.status_code == status.HTTP_200_OK
    assert response.data['message'] == 'Product Updated Successfully'

@pytest.mark.skip
def test_update_product_without_pk(api_client):
    product_id = ''
    url_ = f'/products/{product_id}/'
    payload = {
        "name": "Banknote counter updated"
    }
    response = api_client.patch(url_, data=payload, format='json')
    print(f'status code {response.status_code}')
    assert response.status_code == status.HTTP_404_NOT_FOUND

@pytest.mark.django_db
def test_update_product_empty_payload(api_client, create_product):
    product_id = create_product[0].id
    url_ = f'/products/{product_id}/'
    payload = {}
    response = api_client.patch(url_, data=payload, format='json')
    print(f'status code {response}')
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.data['message'] == 'Request body cannot be empty'
    logger.info(f'Request body cannot be empty {payload}')

@pytest.mark.skip
def test_delete_product(api_client, create_product):
    product_id = create_product[0].id
    print(product_id)
    url_ = f'/products/{product_id}/'
    response = api_client.delete(url_)
    print(f'status code {response.status_code}')
    print(f'Response Data {response.data}')
    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert response.data['message'] == 'Product Deleted Successfully!'


@pytest.mark.skip
def test_delete_product_without_pk(api_client):
    product_id = ''
    url_ = f'/products/{product_id}/'
    response = api_client.delete(url_)
    print(f'status code {response.status_code}')
    assert response.status_code == status.HTTP_404_NOT_FOUND
