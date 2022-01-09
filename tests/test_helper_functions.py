import datetime
from dataclasses import dataclass
from datetime import timedelta
from urllib.parse import urljoin

import faker
import requests
import json
import random

URL = "https://restful-booker.herokuapp.com"


def create_booking_json():
    info, payload = build_json_data()
    headers = {
        'Content-Type': 'application/json'
    }
    return info, headers, payload


def build_json_data():
    fake = faker.Faker()
    info = BookingInfo(first_name=fake.first_name(),
                       last_name=fake.last_name(),
                       price=random.randint(0, 99999),
                       deposit=random.choice([True, False]),
                       check_in=fake.date_time_this_decade(),
                       check_out=fake.date_time_this_decade(),
                       needs=fake.word())
    payload = json.dumps({
        "firstname": info.first_name,
        "lastname": info.last_name,
        "totalprice": info.price,
        "depositpaid": info.deposit,
        "bookingdates": {
            "checkin": str(info.check_in),
            "checkout": str(info.check_out)
        },
        "additionalneeds": info.needs
    })
    return info, payload


def update_booking_json():
    info, payload = build_json_data()
    headers = {
        'Accept': 'application/json',
        'Authorization': 'Basic YWRtaW46cGFzc3dvcmQxMjM=',
        'Content-Type': 'application/json'
    }
    return info, headers, payload


def create_auth_token(password):
    url = urljoin(URL, "auth")
    payload = json.dumps({
      "username": "admin",
      "password": password
    })
    headers = {
      'Content-Type': 'application/json'
    }
    response = requests.request("POST", url, headers=headers, data=payload)
    return json.loads(response.text)['token']


@dataclass
class BookingInfo:
    first_name: str
    last_name: str
    price: int
    deposit: bool
    check_in: datetime.datetime
    check_out: datetime.datetime
    needs: str
