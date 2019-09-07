from flask_restful import Resource
from flask import request

from models.vw_crm_refund_docref import CrmRefundDocrefViewModel
from schemas.vw_crm_refund_docref import CrmRefundDocrefViewSchema

img_schema = CrmRefundDocrefViewSchema()
img_list_schema = CrmRefundDocrefViewSchema(many=True)


class CrmContactRefundListImgUrl(Resource):
    @classmethod
    def get(cls, hyrf_id: int):
        return img_list_schema.dump(CrmRefundDocrefViewModel.find_by_id(hyrf_id)), 200
