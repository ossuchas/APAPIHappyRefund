from db import db
from typing import List


class CrmRefundBankNameListViewModel(db.Model):
    __tablename__ = "vw_crm_refund_banknamelst"

    hyrf_id = db.Column(db.Integer, primary_key=True)
    contractnumber = db.Column(db.String(20))
    contactid = db.Column(db.String(50))
    fullname = db.Column(db.String(255))

    @classmethod
    def find_all(cls) -> List["CrmRefundBankNameListViewModel"]:
        return cls.query.filter_by().all()

    @classmethod
    def find_by_id(cls, _hyrf_id: int) -> "CrmRefundBankNameListViewModel":
        return cls.query.filter_by(hyrf_id=_hyrf_id).first()

    @classmethod
    def find_by_contractno(cls, _contractnumber: str) -> List["CrmRefundBankNameListViewModel"]:
        return cls.query.filter_by(contractnumber=_contractnumber).all()
