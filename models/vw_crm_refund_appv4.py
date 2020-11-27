from db import db
from typing import List
from sqlalchemy.dialects.postgresql import UUID


class CrmRefundAppv4ViewModel(db.Model):
    __tablename__ = "vw_crm_refund_appv4"

    productid = db.Column(db.String(15))
    project = db.Column(db.String(255))
    unitnumber = db.Column(db.String(10))
    contractnumber = db.Column(db.String(20))
    transfernumber = db.Column(db.String(50), primary_key=True)
    transferdateapprove = db.Column(db.DateTime)
    remainingtotalamount = db.Column(db.Float)
    carryaputil = db.Column(db.String(2))
    bringaputil = db.Column(db.Float)
    contactid = db.Column(db.String(50))
    personcardid = db.Column(db.String(20))
    fullname = db.Column(db.String(255))
    nationality = db.Column(db.String(50))
    mobile = db.Column(db.String(100))
    email = db.Column(db.String(255))
    approvedate4 = db.Column(db.DateTime)
    approvedate4text = db.Column(db.String(50))
    approve4by = db.Column(db.String(128))
    refundstatus = db.Column(db.String(200))
    hyrf_id = db.Column(db.Integer)
    doc_merge_url = db.Column(db.String(255))

    # modified by Suchat S. 2020-11-11 for add new transfer id
    transferid = db.Column(UUID(as_uuid=True), nullable=True)

    @classmethod
    def find_all(cls) -> List["CrmRefundAppv4ViewModel"]:
        return cls.query.filter_by().order_by(cls.approvedate4.desc()).all()

    @classmethod
    def find_txt_search_all(cls, str_search: str) -> List["CrmRefundAppv4ViewModel"]:
        return cls.query.filter(
            (cls.unitnumber.like('%' + str_search + '%')) |
            (cls.productid.like('%' + str_search + '%')) |
            (cls.project.like('%' + str_search + '%')) |
            (cls.fullname.like('%' + str_search + '%')) |
            (cls.transfernumber.like('%' + str_search + '%')) |
            (cls.contractnumber.like('%' + str_search + '%'))
        ).order_by(cls.approvedate4.desc()).all()
