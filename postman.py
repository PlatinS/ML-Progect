import requests

data = {
    "tweet": "Thousands gather in Berlin to protest against Covid-19 restrictions"
    }


def send_json(data):
    url = 'http://127.0.0.1:5000/predict'
    headers = {'content-type': 'application/json'}
    response = requests.post(url, json=data, headers=headers)
    return response


if __name__ == '__main__':
    response = send_json(data)
    print(response.json())