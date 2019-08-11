import traceback
from flask_restful import Resource
from flask import request, make_response, render_template
from werkzeug.security import safe_str_cmp
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    jwt_refresh_token_required,
    get_jwt_identity,
    jwt_required,
    get_raw_jwt,
)

from models.crm_contact_refund import CrmContactRefundModel
from schemas.crm_contact_refund import CrmContactRefundSchema

hyrf_schema = CrmContactRefundSchema()
hyrf_list_schema = CrmContactRefundSchema(many=True)


class CrmContactRefund(Resource):
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
            hyrf.tf01_remarks = item_json["tf01_remarks"]
        else:
            return {"message": "Can not find Department ID for update"}, 404

        hyrf.save_to_db()

        return hyrf_schema.dump(hyrf), 200


class CrmContactRefundList(Resource):
    @classmethod
    def get(cls):
        return hyrf_list_schema.dump(CrmContactRefundModel.find_all()), 200



