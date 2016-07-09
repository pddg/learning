from urllib.request import urlopen
from datetime import datetime
import json
from settings import my_lec_list, base_url


class InfoList(object):
    def __init__(self):
        self.json = self.get_api()
        self.table = self.json["table"]
        self.count = self.json["count"]
        self.body = self.json["body"]
        self.my_list = self.set_my_info()

    @staticmethod
    def get_api():
        api = urlopen(base_url + "info/")
        s = api.read().decode('utf-8')
        return json.loads(s)

    @staticmethod
    def identify(subject):
        if subject in my_lec_list:
            return True
        else:
            return False

    def set_ids(self):
        id_list = []
        for b in self.body:
            judge = self.identify(b["subject"])
            if judge:
                id_list.append(b["id"])
            else:
                pass
        return id_list

    def set_my_info(self):
        detail_list = []
        for id in self.set_ids():
            d = InfoDetail(id)
            detail_list.append(d)
        return detail_list


class InfoDetail(object):
    def __init__(self, info_id):
        self.id = info_id
        self.json = self.get_api()
        self.subject = self.json["subject"]
        self.teacher = self.json["teacher"]
        self.abstract = self.json["abstract"]
        self.detail = self.json["detail"]
        self.created_at = self.convert_date(self.json["time"]["created_at"])
        self.last_update = self.convert_date(self.json["time"]["last_update"])
        self.last_confirm = self.convert_date(self.json["time"]["last_confirm"])

    def get_api(self):
        api = urlopen(base_url + "info/id/" + str(self.id))
        s = api.read().decode('utf-8')
        return json.loads(s)

    @staticmethod
    def convert_date(d):
        l = len(d)
        if l > 11:
            return datetime.strptime(d, "%Y/%m/%d %H:%M:%S")
        else:
            return datetime.strptime(d, "%Y/%m/%d")

if __name__ == "__main__":
    i = InfoList()
    for detail in i.my_list:
        print(type(detail))
        print(detail.subject)
        print(detail.created_at.strftime("%Y-%m-%d %H:%M:%S"))
