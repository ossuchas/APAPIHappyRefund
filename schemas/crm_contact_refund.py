from ma import ma
from models.crm_contact_refund import CrmContactRefundModel


class CrmContactRefundSchema(ma.ModelSchema):
    class Meta:
        model = CrmContactRefundModel

