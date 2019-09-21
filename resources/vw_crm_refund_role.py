from flask_restful import Resource

from models.vw_crm_refund_role import CrmRefundRoleViewModel
from schemas.vw_crm_refund_role import CrmRefundRoleViewSchema

role_schema = CrmRefundRoleViewSchema()


class CrmRefundRoleTF01(Resource):
    @classmethod
    def get(cls, user_name: str):
        role = CrmRefundRoleViewModel.check_role_tf01(_user_name=user_name)
        if role:
            # return role_schema.dump(role), 200
            return {"message": "1"}, 200

        return {"message": "0"}, 200
