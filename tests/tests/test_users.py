from tests.functions import base_url, check


def test():
    url = base_url + '/register'

    check(url, 'delete', params={'username': 'test_user', 'password': '123'}, json_response=False)
    check(url, 'post', params={'username': 'test_user', 'password': '123'}, status_code=201,
          result={'username': 'test_user', 'password': '123'})


if __name__ == '__main__':
    test()
