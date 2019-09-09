from flask_restful import Resource
from flask import request

from models.vw_crm_refund_appv4 import CrmRefundAppv4ViewModel
from schemas.vw_crm_refund_appv4 import CrmRefundAppv4ViewSchema

appv4_schema = CrmRefundAppv4ViewSchema()
appv4_list_schema = CrmRefundAppv4ViewSchema(many=True)


class CrmContactRefundAppv4View(Resource):
    @classmethod
    def get(cls):
        return appv4_list_schema.dump(CrmRefundAppv4ViewModel.find_all()), 200
