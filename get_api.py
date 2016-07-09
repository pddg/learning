from urllib.request import urlopen
import json
from settings import my_lec_list


def get_api(URL):
    api = urlopen(URL)
    return api.read().decode('utf-8')


def get_my_info(js):
    lectures = json.loads(js)
    for lecture in lectures['body']:
        if lecture['subject'] in my_lec_list:
            print(lecture['subject'] + ":" + lecture['teacher'])
    else:
        print('終了')
