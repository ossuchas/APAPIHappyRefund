from ma import ma
from models.vw_crm_refund_role import CrmRefundRoleViewModel


class CrmRefundRoleViewSchema(ma.ModelSchema):
    class Meta:
        model = CrmRefundRoleViewModel
