import traceback
from flask_restful import Resource
from flask import request
import json

from libs.authen import APAuthen, APAuthenException
from libs.strings import errmsg


class UserLogin(Resource):
    @classmethod
    def post(cls):
        user_json = request.get_json()
        try:
            response = APAuthen.ap_authen(user_json["username"], user_json["password"], "CRM")
            return json.loads(response.content), 200
        except APAuthenException as e:
            return {"message": str(e)}, 401
        except:
            traceback.print_exc()
            return {"message": "Login Failed"}, 500
