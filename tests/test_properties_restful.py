import json
import random
from datetime import timedelta
from urllib.parse import urljoin

import faker
import pytest
import requests
from hypothesis import given, settings, example
from hypothesis.strategies import text, characters

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
    headers, payload = create_booking_json(first_name=first_name)
    response = requests.request("POST", url, headers=headers, data=payload)


def create_booking_json(first_name):
    fake = faker.Faker()
    last_name = fake.last_name()
    price = random.randint(0, 99999)
    deposit = random.choice([True, False])
    check_in = fake.date_time_this_decade()
    check_out = check_in + timedelta(days=random.randint(0, 240))
    needs = fake.word()
    payload = json.dumps({
        "firstname": first_name,
        "lastname": last_name,
        "totalprice": price,
        "depositpaid": deposit,
        "bookingdates": {
            "checkin": str(check_in),
            "checkout": str(check_out)
        },
        "additionalneeds": needs
    })
    headers = {
        'Content-Type': 'application/json'
    }
    return headers, payload