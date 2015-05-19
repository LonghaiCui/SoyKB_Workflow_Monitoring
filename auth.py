def calculate_request_header(api_key, api_secret, method, url, timestamp, body=None):
    method = method.upper()
    if body:
        str_to_sign = '%s\n%s\n%s\n%s' % (method, url, timestamp, body)
    else:
        str_to_sign = '%s\n%s\n%s' % (method, url, timestamp)
    return calculate_signature_header(api_key, api_secret, str_to_sign)


def calculate_response_header(api_key, api_secret, timestamp, body):
    string_to_sign = '%s\n%s' % (timestamp, body)
    return calculate_signature_header(api_key, api_secret, string_to_sign)


def validate_request_header(api_key, api_secret, auth_header, method, url, body):
    method = method.upper()
    str_to_sign = '%s\n%s\n%s' % (method, url, body)
    auth_header_supposed = calculate_signature_header(api_key, api_secret, str_to_sign)

    return auth_header == auth_header_supposed


def validate_response_header(api_key, api_secret, auth_header, body):
    auth_header_supposed = calculate_signature_header(api_key, api_secret, body)

    return auth_header == auth_header_supposed


def calculate_signature_header(api_key, api_secret, str_to_sign):
    from hashlib import sha1
    import hmac
    import binascii

    hashed = hmac.new(api_secret.encode('utf-8'), str_to_sign, sha1)

    # The signature
    signature = binascii.b2a_base64(hashed.digest())[:-1]
    auth_header = 'EPS %s:%s' % (api_key, signature)
    return auth_header

