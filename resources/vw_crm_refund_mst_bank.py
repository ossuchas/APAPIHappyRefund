from flask_restful import Resource

from models.vw_crm_refund_mst_bank import CrmRefundMasterBankViewModel
from schemas.vw_crm_refund_mst_bank import CrmRefundMasterBankViewSchema

bank_schema = CrmRefundMasterBankViewSchema()
bank_list_schema = CrmRefundMasterBankViewSchema(many=True)


class CrmContactRefundMasterBankView(Resource):
    @classmethod
    def get(cls):
        return bank_list_schema.dump(CrmRefundMasterBankViewModel.find_all()), 200
