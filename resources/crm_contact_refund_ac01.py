from flask_restful import Resource
from flask import request

from models.crm_contact_refund import CrmContactRefundModel
from schemas.crm_contact_refund import CrmContactRefundSchema

hyrf_schema = CrmContactRefundSchema()
hyrf_list_schema = CrmContactRefundSchema(many=True)


class CrmContactRefundListTF02Appv(Resource):
    @classmethod
    def get(cls):
        return hyrf_list_schema.dump(CrmContactRefundModel.find_all_tf02_appv()), 200


class CrmContactRefundListAC01(Resource):
    @classmethod
    def get(cls):
        return hyrf_list_schema.dump(CrmContactRefundModel.find_all_ac01_all()), 200


class CrmContactRefundAC01(Resource):
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
            hyrf.ac01_appv_flag = item_json["ac01_appv_flag"]
            hyrf.ac01_appv_by = item_json["ac01_appv_by"]
            hyrf.ac01_remarks = item_json["ac01_remarks"]
        else:
            return {"message": "Can not find Refund ID for update"}, 404

        hyrf.save_to_db()

        return hyrf_schema.dump(hyrf), 200
