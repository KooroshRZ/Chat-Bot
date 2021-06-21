import json
from typing import ChainMap
import requests
import time

TOKEN = ""
URL = "https://api.telegram.org/bot{}/".format(TOKEN)

init = False
first_side  = 89546715
second_side = 0

def get_url(url):
    response = requests.get(url)
    content = response.content.decode("utf8")
    return content

def get_json_from_url(url):
    content = get_url(url)
    js = json.loads(content)
    return js

def get_updates(offset=None):
    url = URL + "getUpdates"
    if (offset):
        url += "?offset={}".format(offset)
    js = get_json_from_url(url)
    return js

def get_last_update_id(updates):
    update_ids = []
    for update in updates["result"]:
        update_ids.append(int(update["update_id"]))
    return max(update_ids)


def send_message(chat_id, text):
    url = URL + "sendMessage?chat_id=" + str(chat_id) + "&text=" + text
    get_url(url)


def send_sticker(chat_id, sticker):
    url = URL + "sendSticker?chat_id=" + str(chat_id) + "&sticker=" + sticker
    get_url(url)


def send_photo(chat_id, photo, caption):
    url = URL + "sendPhoto?chat_id=" + str(chat_id) + "&photo=" + photo + "&caption=" + caption
    get_url(url)


def send_video(chat_id, video, caption):
    url = URL + "sendVideo?chat_id=" + str(chat_id) + "&video=" + video + "&caption=" + caption
    get_url(url)


def send_animation(chat_id, animation, caption):
    url = URL + "sendAnimation?chat_id=" + str(chat_id) + "&animation=" + animation + "&caption=" + caption
    get_url(url)


def echo_all(updates):

    global init, first_side, second_side
    dest_id = 0
    
    for update in updates['result']:

        sender = update['message']['from']
        name = f"{sender['first_name']} {sender['first_name']} ({sender['username']}) : {chat_id}"
        chat_id = sender['id']

        if not init:

            if first_side == 0:
                first_side = chat_id
            if first_side != chat_id:
                second_side = chat_id
                init = True


        if chat_id == first_side:
            dest_id = second_side
        elif chat_id == second_side:
            dest_id = first_side
        


        if 'text' in update['message']:
            print('text')
            text = update['message']['text']
            sent = f"{name} :\n {text}"
            send_message(chat_id=dest_id, text=text)
            

        elif 'sticker' in update['message']:
            print('sticker')
            sticker_id = update['message']['sticker']['file_id']
            send_sticker(chat_id=dest_id, sticker=sticker_id)


        elif 'animation' in update['message']:
            print('animation')
            animation_id = update['message']['animation']['file_id']
            
            caption = ''
            if 'caption' in update['message']:
                caption = update['message']['caption']

            send_animation(chat_id=dest_id, animation=animation_id, caption=caption)            
            

        elif 'photo' in update['message']:
            print('photo')
            photo_id = update['message']['photo'][1]['file_id']
            
            caption = ''
            if 'caption' in update['message']:
                caption = update['message']['caption']

            send_photo(chat_id=dest_id, photo=photo_id, caption=caption)
            

        elif 'video' in update['message']:
            print('video')
            video_id = update['message']['video']['file_id']

            caption = ''
            if 'caption' in update['message']:
                caption = update['message']['caption']
            
            send_video(chat_id=dest_id, video=video_id, caption=caption)

            

        
def main():
    last_update_id = None

    while True:
        updates = get_updates(last_update_id)
        if len(updates["result"]) > 0:
            last_update_id = get_last_update_id(updates) + 1
            echo_all(updates)
        time.sleep(3)


if __name__ == '__main__':
    main()