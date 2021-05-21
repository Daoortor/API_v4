from tests.functions import base_url, check


def test():
    url = base_url + '/items'
    url_stores = base_url + '/stores'

    check(url_stores + '/test', 'delete', json_response=False)
    check(url_stores + '/test', 'post',
          result={'name': 'test'}, status_code=201)
    check(url_stores + '/test', 'get', result={'name': 'test', 'items': []}, status_code=200)
    check(url + '/sofa', 'post', params={'price': 45000, 'shop_name': 'test'}, result={'name': 'sofa', 'price': 45000,
                                                                                       'shop_name': 'test'},
          status_code=201)
    check(url + '/sofa', 'get', params={'shop_name': 'test'}, result={'name': 'sofa', 'price': 45000}, status_code=200)
    check(url + '/car', 'put', params={'price': 1000000, 'shop_name': 'test'}, result={'name': 'car', 'price': 1000000,
                                                                                       'shop_name': 'test'},
          status_code=201)
    check(url + '/sofa', 'put', params={'price': 44999, 'shop_name': 'test'}, result={'name': 'sofa', 'price': 44999,
                                                                                      'shop_name': 'test'},
          status_code=200)
    check(url, 'post', params={"shop_name": "test", "items": [{"name": "cheese", "price": 160},
                                                              {"name": "sugar", "price": 100}]}, json_request=True,
          result={'items': [{'name': 'cheese', 'price': 160}, {'name': 'sugar', 'price': 100}]}, status_code=201)
    check(url_stores + '/test', 'get', params={'shop_name': 'test'}, status_code=200)
    check(url, 'get')
    check(url + '/car', 'delete', params={'shop_name': 'test'}, status_code=204, json_response=False)
    check(url + '/sofa', 'delete', params={'shop_name': 'test'}, status_code=204, json_response=False)


if __name__ == '__main__':
    test()
