from flask_restful import Resource

from models.vw_crm_refund_banknamelst import CrmRefundBankNameListViewModel
from schemas.vw_crm_refund_banknamelst import CrmRefundBankNameListViewSchema

bankname_schema = CrmRefundBankNameListViewSchema()
bankname_list_schema = CrmRefundBankNameListViewSchema(many=True)


class CrmContactRefundBankNameListView(Resource):
    @classmethod
    def get(cls, hyrf_id: int):
        hyrf = CrmRefundBankNameListViewModel.find_by_id(hyrf_id)
        if hyrf:
            # return bankname_list_schema.dump(hyrf), 200
            return bankname_list_schema.dump(CrmRefundBankNameListViewModel.find_by_contractno(hyrf.contractnumber)), 200

        return {"message": "No Data Found"}, 404
