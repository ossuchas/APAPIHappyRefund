from db import db
from typing import List


class CrmRefundAppv4ViewModel(db.Model):
    __tablename__ = "vw_crm_refund_appv4"

    productid = db.Column(db.String(15))
    project = db.Column(db.String(255))
    unitnumber = db.Column(db.String(10))
    contractnumber = db.Column(db.String(20))
    transfernumber = db.Column(db.String(50), primary_key=True)
    transferdateapprove = db.Column(db.DateTime)
    remainingtotalamount = db.Column(db.Float)
    contactid = db.Column(db.String(50))
    personcardid = db.Column(db.String(20))
    fullname = db.Column(db.String(255))
    nationality = db.Column(db.String(50))
    mobile = db.Column(db.String(100))
    email = db.Column(db.String(255))
    approvedate4 = db.Column(db.DateTime)
    approve4by = db.Column(db.String(128))

    @classmethod
    def find_all(cls) -> List["CrmRefundAppv4ViewModel"]:
        return cls.query.filter_by().all()
