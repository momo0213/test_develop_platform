
import requests
class SendRequest(object):
    '''cookie+session鉴权'''

    def __init__(self):
        self.sess = requests.session()

    def send(self, method, url, headers=None, params=None, json=None, data=None, files=None):
        method = method.lower()
        if method == "post":
            response = self.sess.post(url=url, headers=headers, json=json, data=data, files=files)
        if method == "get":
            response = self.sess.get(url=url, headers=headers, params=params)
        if method == "patch":
            response = self.sess.patch(url=url, headers=headers, json=json, data=data, files=files)
        return response