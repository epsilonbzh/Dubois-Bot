import base64
import json
import random
import time

import requests


class SwsException(Exception):
    pass


class UserSWS:
    user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36 Edg/107.0.1418.62"

    def __init__(self, name, code_etablisement, code_identifiant, code_pin, autosign):
        self.jbauth = None
        self.bearer = None
        self.name = name
        self.code_etablisement = code_etablisement
        self.code_identifiant = code_identifiant
        self.code_pin = code_pin
        self.autosign = autosign
        self.url_image = "data/default.png"
        self.set_jbauth()
        self.set_bearer()
        self.id_classe = -1

    def get_autosign(self):
        return self.autosign

    def get_name(self):
        return self.name

    def set_jbauth(self):
        concatenate = self.code_etablisement + self.code_identifiant + self.code_pin
        self.jbauth = base64.b64encode(concatenate.encode('ascii')).decode("utf-8")

    def get_token_jbauth(self):
        return "JBAuth " + self.jbauth

    def set_bearer(self):
        headers = {'authorization': self.get_token_jbauth(), 'User-Agent': self.user_agent}
        url_get_token = "https://app.sowesign.com/api/portal/authentication/token"
        data = requests.post(url_get_token, headers=headers).content.decode('utf-8')
        tojson = json.loads(data.replace("'", '"'))
        self.bearer = tojson["token"]

    def get_bearer(self):
        return self.bearer

    def get_token_bearer(self):
        return "Bearer " + self.bearer

    def set_id_classe(self):
        headers = {'authorization': self.get_token_bearer(), 'User-Agent': self.user_agent}
        params = {'limit': 12}
        url_check_classes = "https://app.sowesign.com/api/student-portal/future-courses"
        data = requests.get(url_check_classes, params=params, headers=headers).content.decode('utf-8')
        tojson = json.loads(data)
        res = {}
        date = time.strftime("%Y-%m-%d", time.gmtime())

        for classe in tojson:

            id_classe = classe['id']

            if classe['date'] == date:
                res[id_classe] = {}
                res[id_classe]['date'] = classe['date']
                res[id_classe]['start'] = classe['start']
                res[id_classe]['end'] = classe['end']

        current_time = time.strftime("%H:%M:%S", time.gmtime())
        id_classe = -1
        for classe in res:
            if res[classe]['end'] > current_time > res[classe]['start']:
                if id_classe != -1:
                    raise SwsException('tow classes found : ', id_classe, "  and : ", classe)
                id_classe = classe
        if id_classe == -1:
            raise SwsException('no classes found')
        self.id_classe = id_classe

    def find_id_classe(self):
        if self.id_classe == -1:
            self.set_id_classe()

        return self.id_classe

    def get_signer(self):
        toutf8 = self.get_token_bearer().split('.')[1].encode('utf-8')
        tobyte = base64.urlsafe_b64decode(toutf8 + b'==').decode('utf8').replace("'", '"')
        tojson = json.loads(tobyte)
        id_signer = tojson['entity']['id']

        return id_signer

    def signature_to_base64(self):
        fimg = open(self.url_image, "rb")
        img_base64 = base64.b64encode(fimg.read()).decode("utf-8")

        return img_base64

    def get_signature(self):
        headers = {'authorization': self.get_token_bearer(), 'User-Agent': self.user_agent}
        params = {'from': "2022-09-25", 'to': "2022-10-24"}

        url_check_classes = "https://app.sowesign.com/api/student-portal/courses"
        data = requests.get(url_check_classes, params=params, headers=headers).content.decode('utf-8')

        tojson = json.loads(data)

        rnd = random.randint(0, len(tojson) - 1)
        url = tojson[rnd]["signature"]["url"]

        tmpurl = "tmp.png"
        with open(tmpurl, 'wb') as handler:
            handler.write(requests.get(url).content)

        self.url_image = tmpurl
        return self.signature_to_base64()

    def has_signed(self):
        headers = {'authorization': self.get_token_bearer(), 'User-Agent': self.user_agent}
        url_check_classes = "https://app.sowesign.com/api/student-portal/courses/ " + str(
            self.find_id_classe()) + "/assiduity"
        request = requests.get(url_check_classes, headers=headers)
        if request.status_code == 200:
            data = request.content.decode('utf-8')
            tojson = json.loads(data)
            if str(tojson["url"]) != "" and str(tojson["status"]) == "present":
                return True

        return False

    def signature(self):
        if self.has_signed():
            raise SwsException("already sign")

        date = time.strftime("%Y-%m-%dT%H:%M:%S+00:00", time.gmtime())
        json_signature = {"place": 44, "status": "present", "collectMode": "studentPortal", "collectedOn": date,
                          "signedOn": date, "signer": self.get_signer(), "course": self.find_id_classe(),
                          "file": "data:image/png;base64," + self.get_signature()}

        self.send(json_signature=json_signature)

    def save(self):
        date = time.strftime("%Y-%m-%dT%H:%M:%S+00:00", time.gmtime())
        json_signature = {"place": 44, "status": "oupsii", "collectMode": "studentPortal", "collectedOn": date,
                          "signedOn": date, "signer": self.get_signer(), "course": self.find_id_classe()}
        self.send(json_signature=json_signature)

    def send(self, json_signature):
        r = -1
        url = "https://app.sowesign.com/api/student-portal/signatures"

        headers = {'authorization': self.get_token_bearer(), 'User-Agent': self.user_agent}
        try:
            r = requests.post(url, json=json_signature, headers=headers)
            r.raise_for_status()
        except requests.exceptions.HTTPError as err:
            raise SwsException("http error" + r.content.decode("utf-8") + str(err))
