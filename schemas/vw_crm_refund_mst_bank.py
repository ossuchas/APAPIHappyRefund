from ma import ma
from models.vw_crm_refund_mst_bank import CrmRefundMasterBankViewModel


class CrmRefundMasterBankViewSchema(ma.ModelSchema):
    class Meta:
        model = CrmRefundMasterBankViewModel
