import base64
import json
import random
import time

import requests


class UserSWS:
    userAgent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 " \
                "Safari/537.36 Edg/106.0.1370.47 "

    codeEtablisement = ""
    codeIdentifiant = ""
    codePin = ""
    JBAuth = ""
    Bearer = ""
    urlImage = ""
    discord = ""

    def __init__(self, codeEtablisement, codeIdentifiant, codePin):
        self.signed = False
        self.codeEtablisement = codeEtablisement
        self.codeIdentifiant = codeIdentifiant
        self.codePin = codePin
        self.urlImage = "data/default.png"
        self.setJBAuth()
        self.setBearer()
        # todo
        self.signature()

    def setJBAuth(self):
        concatenate = self.codeEtablisement + self.codeIdentifiant + self.codePin
        self.JBAuth = base64.b64encode(concatenate.encode('ascii')).decode("utf-8")

    def getTokenJBAuth(self):
        tokenJBAuth = "JBAuth " + self.JBAuth
        return tokenJBAuth

    def setBearer(self):
        headers = {'authorization': self.getTokenJBAuth(), 'User-Agent': self.userAgent}
        url_get_token = "https://app.sowesign.com/api/portal/authentication/token"
        data = requests.post(url_get_token, headers=headers).content.decode('utf-8')
        tojson = json.loads(data.replace("'", '"'))
        self.Bearer = tojson["token"]

    def getBearer(self):
        return self.Bearer

    def getTokenBearer(self):
        tokenBearer = "Bearer " + self.Bearer
        return tokenBearer

    def checkIdClasses(self):
        headers = {'authorization': self.getTokenBearer(), 'User-Agent': self.userAgent}
        params = {'limit': 12}
        urlCheckClasses = "https://app.sowesign.com/api/student-portal/future-courses"
        data = requests.get(urlCheckClasses, params=params, headers=headers).content.decode('utf-8')
        tojson = json.loads(data)
        res = {}
        date = time.strftime("%Y-%m-%d", time.gmtime())

        for classe in tojson:

            idC = classe['id']

            if classe['date'] == date:
                res[idC] = {}
                res[idC]['date'] = classe['date']
                res[idC]['start'] = classe['start']
                res[idC]['end'] = classe['end']

        current_time = time.strftime("%H:%M:%S", time.gmtime())
        idClasse = -1
        for classe in res:
            if res[classe]['end'] > current_time > res[classe]['start']:
                if idClasse != -1:
                    raise Exception('tow classes found : ', idClasse, "  and : ", classe)
                idClasse = classe
        if idClasse == -1:
            raise Exception('no classes found')
        return idClasse

    def getSigner(self):
        toutf8 = self.getTokenBearer().split('.')[1].encode('utf-8')
        tobyte = base64.urlsafe_b64decode(toutf8 + b'==').decode('utf8').replace("'", '"')
        tojson = json.loads(tobyte)
        id_signer = tojson['entity']['id']

        return id_signer

    def signaturetoBase64(self):
        fimg = open(self.urlImage, "rb")
        img_base64 = base64.b64encode(fimg.read()).decode("utf-8")

        return img_base64

    def getSignature(self):
        headers = {'authorization': self.getTokenBearer(), 'User-Agent': self.userAgent}
        params = {'from': "2022-09-25", 'to': "2022-10-24"}

        urlCheckClasses = "https://app.sowesign.com/api/student-portal/courses"
        data = requests.get(urlCheckClasses, params=params, headers=headers).content.decode('utf-8')

        tojson = json.loads(data)

        rnd = random.randint(0, len(tojson) - 1)
        # print(tojson[rnd]["signature"]["url"])
        url = tojson[rnd]["signature"]["url"]

        tmpurl = "tmp.png"
        with open(tmpurl, 'wb') as handler:
            handler.write(requests.get(url).content)

        self.urlImage = tmpurl
        return self.signaturetoBase64()

    def hasSigned(self):
        return self.signed

    def signature(self):
        r = -1
        url = "https://app.sowesign.com/api/student-portal/signatures"

        date = time.strftime("%Y-%m-%dT%H:%M:%S+00:00", time.gmtime())
        jsonSignature = {"place": 44, "status": "present", "collectMode": "studentPortal", "collectedOn": date,
                         "signedOn": date, "signer": self.getSigner(), "course": self.checkIdClasses(),
                         "file": "data:image/png;base64," + self.getSignature()}

        headers = {'authorization': self.getTokenBearer(), 'User-Agent': self.userAgent}
        try:
            r = requests.post(url, json=jsonSignature, headers=headers)
            r.raise_for_status()
            self.signed = True
        except requests.exceptions.HTTPError as err:
            raise Exception("http error" + r.content.decode("utf-8"))
