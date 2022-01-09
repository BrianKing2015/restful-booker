import json
import random
from datetime import timedelta
from urllib.parse import urljoin

import faker
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
    info.first_name = first_name
    response = requests.request("POST", url, headers=headers, data=payload)


