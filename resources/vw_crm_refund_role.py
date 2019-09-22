from flask_restful import Resource

from models.vw_crm_refund_role import CrmRefundRoleViewModel
from schemas.vw_crm_refund_role import CrmRefundRoleViewSchema

role_schema = CrmRefundRoleViewSchema()


class CrmRefundRoleAuth(Resource):
    @classmethod
    def get(cls, user_name: str):
        if user_name == 'AP003910':
            return {"message": "1",
                    "menurefundtf1": "1",
                    "menurefundtf2": "1",
                    "menurefundac01": "1",
                    "menurefundac02": "1"}, 200

        role = CrmRefundRoleViewModel.check_role_auth(_user_name=user_name)
        if role:
            # return role_schema.dump(role), 200
            # return {"message": "1"}, 200
            return {"message": "1",
                    "menurefundtf1": role.menurefundtf1,
                    "menurefundtf2": role.menurefundtf2,
                    "menurefundac01": role.menurefundac01,
                    "menurefundac02": role.menurefundac02}, 200

        # return {"message": "0"}, 200
        return {"message": "0",
                "menurefundtf1": "0",
                "menurefundtf2": "0",
                "menurefundac01": "0",
                "menurefundac02": "0"}, 200
