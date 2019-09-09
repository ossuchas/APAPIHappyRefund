from ma import ma
from models.vw_crm_refund_appv4 import CrmRefundAppv4ViewModel


class CrmRefundAppv4ViewSchema(ma.ModelSchema):
    class Meta:
        model = CrmRefundAppv4ViewModel
