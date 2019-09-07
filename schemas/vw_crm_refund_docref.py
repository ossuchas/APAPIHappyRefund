from ma import ma
from models.vw_crm_refund_docref import CrmRefundDocrefViewModel


class CrmRefundDocrefViewSchema(ma.ModelSchema):
    class Meta:
        model = CrmRefundDocrefViewModel
