from flask_restful import Resource
from flask import request

from models.crm_contact_refund import CrmContactRefundModel
from schemas.crm_contact_refund import CrmContactRefundSchema

hyrf_schema = CrmContactRefundSchema()
hyrf_list_schema = CrmContactRefundSchema(many=True)


class CrmContactRefundListCSSent(Resource):
    @classmethod
    def get(cls):
        return hyrf_list_schema.dump(CrmContactRefundModel.find_all_cs_sent()), 200


class CrmContactRefundListTF01(Resource):
    @classmethod
    def get(cls):
        return hyrf_list_schema.dump(CrmContactRefundModel.find_all_tf01_all()), 200


class CrmContactRefundSearchTF01(Resource):
    @classmethod
    def get(cls, text_search: str):
        return hyrf_list_schema.dump(CrmContactRefundModel.find_txt_search_cs_sent(text_search)), 200


class CrmContactRefundTF01(Resource):
    @classmethod
    def get(cls, hyrf_id: int):
        hyrf = CrmContactRefundModel.find_by_id(hyrf_id)
        if hyrf:
            return hyrf_schema.dump(hyrf), 200

        return {"message": "No Data Found"}, 404

    @classmethod
    def put(cls, hyrf_id: int):
        item_json = request.get_json()
        hyrf = CrmContactRefundModel.find_by_id(hyrf_id)

        if hyrf:
            hyrf.tf01_appv_flag = item_json["tf01_appv_flag"]
            hyrf.tf01_appv_by = item_json["tf01_appv_by"]
            hyrf.tf01_remarks = item_json["tf01_remarks"]
            hyrf.bankcode = item_json["bankcode"]
            hyrf.bankaccountno = item_json["bankaccountno"].replace('-', '')
            hyrf.bankaccountname = item_json["bankaccountname"]
        else:
            return {"message": "Can not find Refund ID for update"}, 404

        hyrf.save_to_db()

        return hyrf_schema.dump(hyrf), 200
