import base64
import json
import time

import requests


class UserSWS:
    userAgent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 " \
                "Safari/537.36 Edg/106.0.1370.47 "
    jsonSignature = {
        "signedOn": "1970-01-01T01:00:00+00:00",
        "collectedOn": "1970-01-01T01:00:00+00:00",
        "status": "present",
        "collectMode": "studentPortal",
        "signer": -1,
        "course": -1,
        "place": 44,
        "file": "img"
    }

    codeEtablisement = ""
    codeIdentifiant = ""
    codePin = ""
    JBAuth = ""
    Bearer = ""
    urlImage = ""
    discord = ""

    def __init__(self, codeEtablisement, codeIdentifiant, codePin, urlImage, discord):
        self.signed = False
        self.codeEtablisement = codeEtablisement
        self.codeIdentifiant = codeIdentifiant
        self.codePin = codePin
        self.urlImage = urlImage
        self.discord = discord
        self.setJBAuth()
        self.setBearer()
        # todo
        # self.signature()


    def setJBAuth(self):
        concatenate = self.codeEtablisement + self.codeIdentifiant + self.codePin
        self.JBAuth = base64.b64encode(concatenate.encode('ascii')).decode("utf-8")

    def getTokenJBAuth(self):
        tokenJBAuth = "JBAuth " + self.JBAuth
        # print(tokenJBAuth)
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
        # print(tokenBearer)
        return tokenBearer

    def checkIdClasses(self):
        headers = {'authorization': self.getTokenBearer(), 'User-Agent': self.userAgent}
        params = {'limit': 12}
        urlCheckClasses = "https://app.sowesign.com/api/student-portal/future-courses"
        data = requests.get(urlCheckClasses, params=params, headers=headers).content.decode('utf-8')
        tojson = json.loads(data.replace("'", '"'))

        res = {}
        date = time.strftime("%Y-%m-%d", time.gmtime())

        for classe in tojson:

            id = classe['id']

            if classe['date'] == date:
                res[id] = {}
                res[id]['date'] = classe['date']
                res[id]['start'] = classe['start']
                res[id]['end'] = classe['end']

        current_time = time.strftime("%H:%M:%S", time.gmtime())
        idClasse = -1
        for classe in res:
            if res[classe]['end'] > current_time > res[classe]['start']:
                if idClasse != -1:
                    raise Exception('tow classes found : ', idClasse, "  and : ", classe)
                idClasse = classe
        return idClasse

    def getSigner(self):
        toutf8 = self.getTokenBearer().split('.')[1].encode('utf-8')
        tobyte = base64.urlsafe_b64decode(toutf8 + b'==').decode('utf8').replace("'", '"')
        tojson = json.loads(tobyte)
        id_signer = tojson['entity']['id']

        return id_signer

    def hasSigned(self):
        return self.signed

    def signature(self):
        url = "https://app.sowesign.com/api/student-portal/signatures"

        fimg = open("data/" + self.urlImage, "rb")
        img_base64 = base64.b64encode(fimg.read()).decode("utf-8")

        date = time.strftime("%Y-%m-%dT%H:%M:%S+00:00", time.gmtime())

        self.jsonSignature["collectedOn"] = date
        self.jsonSignature["signedOn"] = date
        self.jsonSignature["signer"] = self.getSigner()
        self.jsonSignature["course"] = self.checkIdClasses()
        self.jsonSignature["file"] = "data:image/png;base64," + img_base64

        headers = {'authorization': self.getTokenBearer(), 'User-Agent': self.userAgent}
        try:
            r = requests.post(url, json=self.jsonSignature, headers=headers)
            r.raise_for_status()
            self.signed = True
        except requests.exceptions.HTTPError as err:
            raise Exception("http error" + r.content.decode("utf-8"))
            # await ctx.send(r)
            # await ctx.send(r.content)
            # print(r)
            # print(r.content)
