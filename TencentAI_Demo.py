#-*- coding: UTF-8 -*-
import sys
sys.path.append('./SDK')
import apiutil
import json
import os
import hashlib
import base64


# 这里填写申请好的key和id
app_key = 'XXXXXXXXXXX'
app_id = 'XXXXXXXXXX'


def test_ocr_generalocr(filepath):
    with open(filepath, 'rb') as bin_data:
        image_data = bin_data.read()

    ai_obj = apiutil.AiPlat(app_id, app_key)

    print('----------------------SEND REQ----------------------')
    rsp = ai_obj.getOcrGeneralocr(image_data)

    if rsp['ret'] == 0:
        for i in rsp['data']['item_list']:
            print(i['itemstring'])
        print('----------------------API SUCC----------------------')
    else:
        print(json.dumps(rsp, ensure_ascii=False, sort_keys=False, indent=4))
        print('----------------------API FAIL----------------------')


def test_nlp_texttrans():
    str_text = '今天天气怎么样'
    type = 0
    ai_obj = apiutil.AiPlat(app_id, app_key)

    print('----------------------SEND REQ----------------------')
    rsp = ai_obj.getNlpTextTrans(str_text, type)
    if rsp['ret'] == 0:
        print(json.dumps(rsp, ensure_ascii=False, sort_keys=False, indent=4))
        print('----------------------API SUCC----------------------')
    else:
        print(json.dumps(rsp, ensure_ascii=False, sort_keys=False, indent=4))
        print('----------------------API FAIL----------------------')


def test_aai_wxasrs():
    seq = 0
    for_mat = 8
    rate = 16000
    bits = 16
    cont_res = 1
    once_size = 6400
    file_path = './data/wxasrs.mp3'
    f = open(file_path, 'rb')
    md5obj = hashlib.md5()
    md5obj.update(f.read())
    hash = md5obj.hexdigest()
    speech_id = str(hash).upper()
    f.close()
    f = open(file_path, 'rb')
    file_size = os.path.getsize(file_path)
    try:
        while True:
            chunk = f.read(once_size)
            if not chunk:
                break
            else:
                chunk_size = len(chunk)
                if (seq + chunk_size) == file_size:
                    end = 1
                else:
                    end = 0

            ai_obj = apiutil.AiPlat(app_id, app_key)

            print('----------------------SEND REQ----------------------')
            rsp = ai_obj.getAaiWxAsrs(chunk, speech_id, end, for_mat, rate, bits, seq, chunk_size, cont_res)
            seq += chunk_size
            if rsp['ret'] == 0:
                print(json.dumps(rsp, ensure_ascii=False, sort_keys=False, indent=4))
                print('----------------------API SUCC----------------------')
            else:
                print(json.dumps(rsp, ensure_ascii=False, sort_keys=False, indent=4))
                print('----------------------API FAIL----------------------')
    finally:
        f.close()


def test_aai_ailab(text='今天天气怎么样'):
    speaker = 1
    for_mat = {
        "PCM": 1,
        "WAV": 2,
        "MP3": 3
        }
    volume = 0
    speed = 100
    #text = '今天天气怎么样'
    aht = 0
    apc = 58
    ai_obj = apiutil.AiPlat(app_id, app_key)

    print('----------------------SEND REQ----------------------')
    rsp = ai_obj.getAaiAiLab(speaker, for_mat['WAV'], volume, speed, text, aht, apc)
    if rsp['ret'] == 0:
        print(json.dumps(rsp, ensure_ascii=False, sort_keys=False, indent=4))
        speech = rsp['data']['speech']
        speech = base64.b64decode(speech)
        md5sum = rsp['data']['md5sum']
        has_md5 = hashlib.md5(speech)
        speech_md5 = has_md5.hexdigest().upper()
        if md5sum == speech_md5:
            with open('./data/ailab.wav', 'wb') as f:
                f.write(speech)
        print('----------------------API SUCC----------------------')
    else:
        print(json.dumps(rsp, ensure_ascii=False, sort_keys=False, indent=4))
        print('----------------------API FAIL----------------------')

def test_aai_youtu():
    speed = 0
    text = '今天天气怎么样'
    model_type = 0
    ai_obj = apiutil.AiPlat(app_id, app_key)

    print('----------------------SEND REQ----------------------')
    rsp = ai_obj.getAaiYoutu(speed, text, model_type)
    if rsp['ret'] == 0:
        print(json.dumps(rsp, ensure_ascii=False, sort_keys=False, indent=4))
        speech = rsp['data']['voice']
        speech = base64.b64decode(speech)
        with open('./data/youtu.mp3', 'wb') as f:
            f.write(speech)
        print('----------------------API SUCC----------------------')
    else:
        print(json.dumps(rsp, ensure_ascii=False, sort_keys=False, indent=4))
        print('----------------------API FAIL----------------------')


if __name__ == '__main__':
    path = './data/generalocr.jpg'
    test_ocr_generalocr(path)
    test_aai_wxasrs()
    test_nlp_texttrans()
    test_aai_ailab()
    test_aai_youtu()
