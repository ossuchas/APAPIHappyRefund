from db import db
from typing import List


class CrmRefundMasterBankViewModel(db.Model):
    __tablename__ = "vw_crm_refund_mst_bank"

    bankid = db.Column(db.String(15), primary_key=True)
    bankname = db.Column(db.String(255))
    adbankname = db.Column(db.String(15))

    @classmethod
    def find_all(cls) -> List["CrmRefundMasterBankViewModel"]:
        return cls.query.filter_by().all()
