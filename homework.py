import logging
import os
import time

import requests
from dotenv import load_dotenv
from twilio.rest import Client

load_dotenv()
# Переменные среды и константы ВК
VK_API_VERSION = 5.92
vk_access_token = os.getenv('VK_TOKEN')

# Переменные среды аккаунта Twillo
account_sid = os.getenv('ACCOUNT_SID')
auth_token = os.getenv('TWILLO_AUTH_TOKEN')
twillo_from_number = os.getenv('NUMBER_FROM')
twillo_to_number = os.getenv('NUMBER_TO')
twill_client = Client(account_sid, auth_token)

# Включаем поддержку записи UTF-8 в журналах
logging.basicConfig(
    handlers=[logging.FileHandler('api_01_sms.log', 'w', 'utf-8')],
    format="%(filename)s[LINE:%(lineno)d]# "
           "%(levelname)-8s [%(asctime)s]  %(message)s",
    level=logging.INFO
)


def get_status(user_id):
    params = {
        'access_token': vk_access_token,
        'fields': 'online',
        'user_ids': user_id,
        'v': VK_API_VERSION,
    }
    try:
        response = requests.post(
            'https://api.vk.com/method/users.get',
            params=params
        )
    except requests.exceptions.RequestException as e:
        logging.error(f'Не удалось подключиться к серверу: {e}')
        return 0
    except Exception as e:
        logging.error(f'Ошибка подключения к VK API: {e}')
        return 0
    try:
        response = response.json()['response'][0]
    except KeyError:
        logging.error('Не удается прочитать ответ сервера')
        return 0
    if 'online' in response:
        response = response['online']
        return response
    else:
        logging.error('В ответе сервера не найден искомый параметр')
        return 0


def sms_sender(sms_text):
    try:
        message = twill_client.messages.create(
            body=sms_text,
            from_=twillo_from_number,
            to=twillo_to_number
        )
    except Exception as e:
        logging.error(f'Ошибка подключения к сервису Twillo: {e}')
        return e
    return message.sid


if __name__ == '__main__':
    vk_id = input("Введите id ")
    while True:
        if get_status(vk_id) == 1:
            sms_sender(f'{vk_id} сейчас онлайн!')
            break
        time.sleep(5)
