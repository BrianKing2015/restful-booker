from urllib.parse import urljoin

import requests
import json

from tests.test_helper_functions import create_booking_json, create_auth_token, update_booking_json

'''This is meant to be run with Python pytest version 6.2.4
Commandline usage:
pip install -r requirements.txt
pytest test_restful_booker.py

Should collect 6 tests and run in a little under 3s.
'''


URL = "https://restful-booker.herokuapp.com"


def test_service_up():
    url = urljoin(URL, "ping")
    response = requests.request("GET", url)
    assert response.status_code == 201
    assert response.text == "Created"


def test_bookings_return():
    url = urljoin(URL, "booking")
    response = requests.request("GET", url)
    assert response.status_code == 200
    assert len(response.text) > 1
    assert json.loads(response.text)[0]['bookingid']


def test_creating_booking():
    url = urljoin(URL, "booking")
    info, headers, payload = create_booking_json()
    response = requests.request("POST", url, headers=headers, data=payload)
    json_response = json.loads(response.text)
    assert response.status_code == 200
    assert json_response['booking']['firstname'] == info.first_name
    assert json_response['booking']['lastname'] == info.last_name
    assert json_response['booking']['totalprice'] == info.price
    assert json_response['booking']['depositpaid'] == info.deposit
    assert json_response['booking']['bookingdates']['checkin'] == str(info.check_in).split(' ')[0]
    assert json_response['booking']['bookingdates']['checkout'] == str(info.check_out).split(' ')[0]
    assert json_response['booking']['additionalneeds'] == info.needs


def test_search_by_name():
    booking_id_list = []
    create_booking_url = urljoin(URL, "booking")
    info, headers, payload = create_booking_json()
    create_call = requests.request("POST", create_booking_url, headers=headers, data=payload)
    json_create_call = json.loads(create_call.text)

    search_url = urljoin(URL, f"booking?firstname={info.first_name}&lastname={info.last_name}")
    search_call = requests.request("GET", search_url)
    json_search_booking_call = json.loads(search_call.text)

    for entry in json_search_booking_call:
        booking_id_list.append(entry['bookingid'])
    assert json_create_call['bookingid'] in booking_id_list


def test_update_booking():
    create_booking_url = urljoin(URL, "booking")
    info, headers, payload = create_booking_json()
    create_call = requests.request("POST", create_booking_url, headers=headers, data=payload)
    json_create_call = json.loads(create_call.text)

    auth_token = create_auth_token('password123')
    update_booking_url = urljoin(URL, f"booking/{json_create_call['bookingid']}")
    info, headers, payload = update_booking_json()
    update_call = requests.request("PUT", update_booking_url, headers=headers, data=payload)
    json_response = json.loads(update_call.text)
    assert update_call.status_code == 200
    assert json_response['firstname'] == info.first_name
    assert json_response['lastname'] == info.last_name
    assert json_response['totalprice'] == info.price
    assert json_response['depositpaid'] == info.deposit
    assert json_response['bookingdates']['checkin'] == str(info.check_in).split(' ')[0]
    assert json_response['bookingdates']['checkout'] == str(info.check_out).split(' ')[0]
    assert json_response['additionalneeds'] == info.needs


def test_delete_booking():
    create_booking_url = urljoin(URL, "booking")
    info, headers, payload = create_booking_json()
    create_call = requests.request("POST", create_booking_url, headers=headers, data=payload)
    json_create_call = json.loads(create_call.text)

    delete_url = urljoin(URL, f"booking/{json_create_call['bookingid']}")
    headers = {
        'Accept': 'application/json',
        'Authorization': 'Basic YWRtaW46cGFzc3dvcmQxMjM=',
        'Content-Type': 'application/json'
    }
    delete_response = requests.request("DELETE", delete_url, headers=headers)
    assert delete_response.status_code == 201
    search_by_id_url = urljoin(URL, f"booking/{json_create_call['bookingid']}")
    search_by_id_response = requests.request("get", search_by_id_url)
    assert search_by_id_response.status_code == 404
