import requests
from ast import literal_eval

from confidential import ADMIN


base_url = 'http://localhost:9998'


def get_token():
    response = requests.post(base_url + '/auth', ADMIN, headers={'Content-Type': 'application/json'}).json()
    return response['access_token']


def ordered(obj):
    if isinstance(obj, dict):
        return sorted((k, ordered(v)) for k, v in obj.items())
    if isinstance(obj, list):
        return sorted(ordered(x) for x in obj)
    else:
        return obj


# Compare jsons without taking list element order into account
def json_cmp(data_1, data_2):
    return ordered(data_1) == ordered(data_2)


def check(url, method, params=None, headers=None, status_code=None, result=None, jwt=True, json_request=False,
          json_response=True):
    # Check if JWT is enabled for this test
    if jwt:
        access_token = get_token()
        # Add token to headers
        if headers:
            headers['Authorization'] = 'JWT ' + access_token
        else:
            headers = {'Authorization': 'JWT ' + access_token}
    print(method, url)
    if json_response:
        response = requests.request(method, url, json=params, headers=headers)
    else:
        response = requests.request(method, url, params=params, headers=headers)
    print(response.status_code, response.content)
    # Check conditions
    assert response.status_code == status_code or not status_code

    if not result:
        # Check if response is expected in json format
        if json_response:
            return response.json()
        else:
            return response.content

    if json_response:
        assert json_cmp(response.json(), result)
    else:
        assert response.content == result

    if json_response:
        return response.json()
    else:
        return response.content
