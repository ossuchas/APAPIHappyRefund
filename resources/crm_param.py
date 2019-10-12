from flask_restful import Resource
from flask import request, make_response, render_template

from models.crm_param import CrmParameterModel
from schemas.crm_param import CrmParameterSchema

param_schema = CrmParameterSchema()
param_list_schema = CrmParameterSchema(many=True)


class CrmParameter(Resource):
    @classmethod
    def get(cls, _param_id: int):
        param = CrmParameterModel.find_by_id(_param_id)
        if param:
            return param_schema.dump(), 200

        return {"message": "No Data Found"}, 404

    @classmethod
    def put(cls, _param_id: int):
        item_json = request.get_json()
        param = CrmParameterModel.find_by_id(_param_id)

        # if hyrf:
        #     hyrf.tf01_appv_flag = item_json["tf01_appv_flag"]
        #     hyrf.tf01_appv_by = item_json["tf01_appv_by"]
        #     hyrf.tf01_remarks = item_json["tf01_remarks"]
        # else:
        #     return {"message": "Can not find Department ID for update"}, 404

        param.save_to_db()

        return param_list_schema.dump(param), 200


class CrmParameterList(Resource):
    @classmethod
    def get(cls):
        return param_list_schema.dump(CrmParameterModel.find_by_code()), 200

