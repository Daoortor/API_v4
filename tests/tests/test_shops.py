from tests.functions import base_url, check
from confidential import ADMIN


def test():
    url = base_url + '/stores'
    url_items = base_url + '/items'

    check(url + '/test', 'delete', json_response=False)
    check(url + '/test', 'post', params={'username': eval(ADMIN)['username'], 'password': eval(ADMIN)['password']},
          result={'name': 'test', 'owner': eval(ADMIN)['username']}, status_code=201)
    check(url_items + '/milk', method='post', params={'price': 90, 'shop_name': 'test'})
    check(url + '/test', 'get', result={'name': 'test', 'items': [{'name': 'milk', 'price': 90.0}]}, status_code=200)
    check(url + '/perekrestok', 'post', params={'username': eval(ADMIN)['username'],
                                                'password': eval(ADMIN)['password']})
    check(url_items + '/chocolate', method='post', params={'price': 60, 'shop_name': 'perekrestok'})
    check(url + '/perekrestok', 'get', result={'name': 'perekrestok', 'items': [{'name': 'chocolate', 'price': 60.0}]},
          status_code=200)
    check(url, 'get', result={'stores': [{'name': 'test', 'items': [{'name': 'milk', 'price': 90.0}]},
                                         {'name': 'perekrestok', 'items': [{'name': 'chocolate', 'price': 60.0}]}]},
          status_code=200)


if __name__ == '__main__':
    test()
