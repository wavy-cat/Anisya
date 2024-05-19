import json
from os import environ

from nacl.signing import VerifyKey
from nacl.exceptions import BadSignatureError

from modules.animal import animal
from modules.waifu import waifu


def verify_sign(signature, timestamp, body) -> bool:
    verify_key = VerifyKey(bytes.fromhex(environ['PUBLIC_KEY']))
    try:
        verify_key.verify(f'{timestamp}{body}'.encode(), bytes.fromhex(signature))
    except BadSignatureError:
        return False

    return True


def handler(event, context):
    sign_status = verify_sign(event['headers']["X-Signature-Ed25519"],
                              event['headers']["X-Signature-Timestamp"],
                              event['body'])
    if not sign_status:
        return {'statusCode': 401, 'body': 'invalid request signature'}

    body = json.loads(event['body'])

    if body['type'] == 1:
        return {
            'statusCode': 200,
            'headers': {"Content-Type": "application/json"},
            'body': {'type': 1}
        }

    match body['data']['name']:
        case 'animal':
            return animal(body)
        case 'waifu':
            return waifu(body)
        case _:
            print(f'Used unregistered command {body['data']['name']}. '
                  f'User: {body['user']['username']} ({body['user']['id']})')
            return {
                'statusCode': 200,
                'headers': {'Content-Type': 'application/json'},
                'body': {'type': 4,
                         'data': {'content': 'Oops! I think you used unregistered command.'}}
            }
