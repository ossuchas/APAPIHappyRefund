from ma import ma
from models.vw_crm_refund_banknamelst import CrmRefundBankNameListViewModel


class CrmRefundBankNameListViewSchema(ma.ModelSchema):
    class Meta:
        model = CrmRefundBankNameListViewModel
