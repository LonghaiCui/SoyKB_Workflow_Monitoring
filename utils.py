import json
import requests
from datetime import datetime
from dateutil import tz

import auth
#string = datetime.utcnow().replace(tzinfo=tz.tzutc()).isoformat()

def timestamp_string():
    string = datetime.utcnow().replace(tzinfo=tz.tzutc()).isoformat()
    return string


def build_auth_headers(method, uri, payload=None, api_auth=None, timestamp=None):
        if timestamp is None:
            timestamp = timestamp_string()
        if method == 'GET':
            auth_string = auth.calculate_request_header(api_auth['key'], api_auth['secret'], 'GET', uri, timestamp)
        else:
            auth_string = auth.calculate_request_header(api_auth['key'], api_auth['secret'], 'POST', uri, timestamp,
                                                        payload)
        return {'Authorization': auth_string, 'x-eps-timestamp': timestamp}


class APIRequest(object):
    def __init__(self, url="https://www.naradametrics.net", uri=None, method="POST", payload=None, api_auth=None, file_name="active"):
        if payload:
            try:
                self.payload = json.dumps(payload)
            except TypeError:
                self.payload = payload
        else:
            self.payload = None
        if api_auth:
            self.headers = build_auth_headers(method, uri, self.payload, api_auth)
        else:
            self.headers = None
        methodmap = {'POST': requests.post, 'GET': requests.get}
        try:
            self.response = methodmap[method](url + uri, data=self.payload, headers=self.headers, verify=False)
        except Exception as e:
            print 'API_request_error: %s' % e
            f = open(file_name+ ".txt", 'a')
            f.write(str(payload)+'\n')
            f.close()


def typecast_dictionary(data, result_format):
    result_list = []
    type_map = {"string": str, "float": float, "integer": int}
    if type(data) is dict:
        data = [data]
    for item in data:
        dictionary = {}
        for key in item:
            try:
                dictionary[key] = type_map[result_format[key]](item[key])
            except KeyError:
                pass
            except ValueError:
                dictionary[key] = str(item[key])
        result_list.append(dictionary)
    return result_list


