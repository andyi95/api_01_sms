import os
import time
import requests

from dotenv import load_dotenv
from twilio.rest import Client

load_dotenv()


def get_status(user_id):
    params = {
        'access_token': os.getenv('VK_TOKEN'),
        'fields': 'online',
        'user_ids': user_id,
        'v': 5.92,
    }
    response = requests.post(
        'https://api.vk.com/method/users.get',
        params=params
    )
    response = response.json()['response'][0]
    response = response['online']
    return response


def sms_sender(sms_text):
    account_sid = os.getenv('ACCOUNT_SID')
    auth_token = os.getenv('TWILLO_AUTH_TOKEN')
    client = Client(account_sid, auth_token)
    message = client.messages.create(
        body=sms_text,
        from_=os.getenv('FROM_PHONE'),
        to=os.getenv('TO_PHONE'),
    )
    return message.sid


if __name__ == "__main__":
    vk_id = input("Введите id ")
    while True:
        if get_status(vk_id) == 1:
            sms_sender(f'{vk_id} сейчас онлайн!')
            break
        time.sleep(5)
