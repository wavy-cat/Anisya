import json
import random

import requests


def get_image_url(animal: str) -> str:
    """Available animals: `animal_cat`, `animal_dog`"""
    match animal:
        case 'animal_cat':
            raw_data = requests.get('https://api.thecatapi.com/v1/images/search').text
        case 'animal_dog':
            raw_data = requests.get('https://api.thedogapi.com/v1/images/search').text
        case _:
            raise 'Unknown animal'

    return json.loads(raw_data)[0]['url']


def animal(body):
    if body['data']['options'][0]['value'] in ('animal_cat', 'animal_dog'):
        image_url = get_image_url(body['data']['options'][0]['value'])
    else:
        image_url = get_image_url(random.choice(['animal_cat', 'animal_dog']))

    return {
        'statusCode': 200,
        'headers': {"Content-Type": "application/json"},
        'body': {'type': 4,
                 'data': {"content": image_url}}
    }
