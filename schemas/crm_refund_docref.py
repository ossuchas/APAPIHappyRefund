from ma import ma
from models.crm_refund_docref import CrmRefundDocrefModel


class CrmRefundDocrefSchema(ma.ModelSchema):
    class Meta:
        model = CrmRefundDocrefModel
