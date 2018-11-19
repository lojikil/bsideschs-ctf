import binascii

import requests


SERVER = 'localhost:8080'

resp = requests.post(
    "http://{0}/api-token".format(SERVER),
    data={"user": "becca", "password": "908ygiw42*ho3iu98fx"}
)
assert resp.status_code == 200
token = resp.content

resp = requests.get(
    "http://{0}/flag".format(SERVER), headers={"X-AUTH-TOKEN": token}
)
print(resp.content)
assert resp.status_code == 403

data = binascii.unhexlify(token)
mutable_data = bytearray(data)
mutable_data[26] ^= ord("0")
mutable_data[26] ^= ord("1")
admin_token = binascii.hexlify(mutable_data)
resp = requests.get(
    "http://{0}/flag".format(SERVER), headers={"X-AUTH-TOKEN": admin_token}
)
assert resp.status_code == 200
print(resp.content)
