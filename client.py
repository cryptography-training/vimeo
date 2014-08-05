import requests

url = "http://localhost:4242/api"
data = {
    'method': 'vimeo.test.login',
    'api_key': raw_input("api_key: "),
    'api_sig': raw_input("api_sig: "),
}
r = requests.post(url, data=data)
print r.text
