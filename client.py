import requests

HOST = 'http://localhost:5000'

response = requests.post(f'{HOST}/users/', json={'name': '0', 'mail': '0@mail.com', "password": '0'})
print(response.status_code)
print(response.text)

response = requests.get(f'{HOST}/users/10')
print(response.status_code)
print(response.text)

# response = requests.get(f'{HOST}/users/')
# print(response.status_code)
# print(response.text)
#
# response = requests.patch(f'{HOST}/users/7', json={"name": "4", "mail": "4@mail.com", "password": "4", "new_password": "4_has_patched"})
# print(response.status_code)
# print(response.text)
#
# response = requests.delete(f'{HOST}/users/8', json={"password": "0"})
# print(response.status_code)
# print(response.text)


# response = requests.post(f'{HOST}/adv/', json={"owner": "0", "mail": "0@mail.com", "password": "0",
#                                                 "title": "Text title",
#                                                 "description": "description test!"})
# print(response.status_code)
# print(response.text)
#
#
# response = requests.patch(f'{HOST}/adv/1', json={"owner": "0", "mail": "0@mail.com", "password": "0",
#                                                 "title": "new Text title",
#                                                 "description": "new description test!"})
# print(response.status_code)
# print(response.text)


response = requests.get(f'{HOST}/adv/')
print(response.status_code)
print(response.text)

response = requests.delete(f'{HOST}/adv/1', json={"owner": "0", "mail": "0@mail.com", "password": "0"})
print(response.status_code)
print(response.text)


