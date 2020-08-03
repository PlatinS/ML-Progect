import requests

data = {
    "tweet": "Coronavirus cases around the globe have surpassed 17.8 million. More than 4.6 million infections have been recorded in the United States."
    }


def send_json(data):
    url = 'http://127.0.0.1:5000/predict'
    headers = {'content-type': 'application/json'}
    response = requests.post(url, json=data, headers=headers)
    return response


if __name__ == '__main__':
    response = send_json(data)
    print(response.json())