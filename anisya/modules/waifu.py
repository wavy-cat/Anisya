import json

import requests


def waifu(body):
    category = body['data']['options'][0]['value']
    raw_data = requests.get('https://api.waifu.pics/sfw/' + category).text
    url = json.loads(raw_data)['url']

    return {
        'statusCode': 200,
        'headers': {"Content-Type": "application/json"},
        'body': {'type': 4,
                 'data': {"content": url}}
    }
