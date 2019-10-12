from flask_restful import Resource
from flask import request
import datetime

from models.crm_contact_refund import CrmContactRefundModel
from schemas.crm_contact_refund import CrmContactRefundSchema

hyrf_schema = CrmContactRefundSchema()
hyrf_list_schema = CrmContactRefundSchema(many=True)


class CrmContactRefundListAC02Appv(Resource):
    @classmethod
    def get(cls):
        return hyrf_list_schema.dump(CrmContactRefundModel.find_all_ac02_appv()), 200


class CrmContactRefundAC03(Resource):
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
            if item_json["ac03_reject_doc_flag"] == 'Y':
                # Reject Document
                hyrf.ac03_reject_doc_flag = 'Y'
                hyrf.ac03_change_due_flag = 'N'
                hyrf.ac03_change_due_date = None
                hyrf.ac03_reject_reason = item_json["ac03_reject_reason"]
            else:
                # Change Due Refund Date
                hyrf.ac03_reject_doc_flag = 'N'
                hyrf.ac03_change_due_flag = 'Y'
                obj = item_json["ac03_change_due_date"]
                hyrf.ac03_change_due_date = "{}-{}-{}".format(obj["year"], obj["month"], obj["day"])
                hyrf.ac02_due_date = "{}-{}-{}".format(obj["year"], obj["month"], obj["day"])
                hyrf.ac03_reject_reason = None

            # hyrf.ac03_reject_doc_flag = item_json["ac03_reject_doc_flag"]
            hyrf.ac02_appv_by = item_json["ac02_appv_by"]
            hyrf.ac02_remarks = item_json["ac02_remarks"]
        else:
            return {"message": "Can not find Refund ID for update"}, 404

        hyrf.save_to_db()

        return hyrf_schema.dump(hyrf), 200


class CrmContactRefundAC03Reject(Resource):
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
            hyrf.ac02_appv_flag = item_json["ac02_appv_flag"]
            hyrf.ac02_appv_by = item_json["ac02_appv_by"]
            hyrf.ac02_remarks = item_json["ac02_remarks"]
        else:
            return {"message": "Can not find Refund ID for update"}, 404

        hyrf.save_to_db()

        return hyrf_schema.dump(hyrf), 200
