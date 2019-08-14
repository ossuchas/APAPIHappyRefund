import os
from typing import List
from requests import Response, post
import json
from libs.strings import errmsg


class APAuthenException(Exception):
    def __init__(self, message: str):
        super().__init__(message)


class APAuthen:

    APAUTHEN_URL = os.environ.get("APAUTHEN_URL")
    APAUTHEN_API_KEY = os.environ.get("APAUTHEN_API_KEY")
    APAUTHEN_API_TOKEN = os.environ.get("APAUTHEN_API_TOKEN")

    @classmethod
    def ap_authen(cls, username: str, password: str, appcode: str) -> Response:
        url = cls.APAUTHEN_URL
        payload = {
            "UserName": username,
            "Password": password,
            "Appcode": appcode
        }
        headers = {
            'Content-Type': 'application/json',
            'api_key': f"{cls.APAUTHEN_API_KEY}",
            'api_token': f"{cls.APAUTHEN_API_TOKEN}"
        }
        response = post(url, data=json.dumps(payload), headers=headers)

        if response.status_code != 200:
            raise APAuthenException(errmsg("authen_failed_status_code"))

        obj = json.loads(response.content)

        if not obj["loginResult"]:
            raise APAuthenException(errmsg("authen_failed"))

        return response
