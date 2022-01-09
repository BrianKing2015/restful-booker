import json
from urllib.parse import urljoin

import pytest
import requests
from hypothesis import given, settings, example
from hypothesis.strategies import text, characters

from tests.test_helper_functions import create_booking_json

URL = "https://restful-booker.herokuapp.com"


@pytest.mark.PROPERTY_TEST
@given(
    first_name=text(
        alphabet=characters(min_codepoint=32, max_codepoint=1000, blacklist_categories=("Cc", "Cs")),
        min_size=0,
        max_size=256,
    )
)
@example("Peter")
@settings(max_examples=3, deadline=2000)
def test_name_properties(first_name):
    url = urljoin(URL, "booking")
    info, headers, payload = create_booking_json()
    over_write_payload = json.loads(payload)
    over_write_payload["firstname"] = first_name
    payload = json.dumps(over_write_payload)
    response = requests.request("POST", url, headers=headers, data=payload)
    json_response = json.loads(response.text)
    assert response.status_code == 200
    assert json_response['booking']['firstname'] == first_name


@pytest.mark.PROPERTY_TEST
@given(
    last_name=text(
        alphabet=characters(min_codepoint=32, max_codepoint=1000, blacklist_categories=("Cc", "Cs")),
        min_size=0,
        max_size=256,
    )
)
@example("Parker")
@settings(max_examples=3, deadline=2000)
def test_name_properties(last_name):
    url = urljoin(URL, "booking")
    info, headers, payload = create_booking_json()
    over_write_payload = json.loads(payload)
    over_write_payload["lastname"] = last_name
    payload = json.dumps(over_write_payload)
    response = requests.request("POST", url, headers=headers, data=payload)
    json_response = json.loads(response.text)
    assert response.status_code == 200
    assert json_response['booking']['lastname'] == last_name


