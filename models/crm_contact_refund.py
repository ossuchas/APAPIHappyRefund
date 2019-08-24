from db import db
from typing import List


class CrmContactRefundModel(db.Model):
    __tablename__ = "crm_contact_refund"

    hyrf_id = db.Column(db.Integer, primary_key=True)
    productid = db.Column(db.String(15))
    project = db.Column(db.String(255))
    unitnumber = db.Column(db.String(10))
    wbsnumber = db.Column(db.String(30))
    contractnumber = db.Column(db.String(20))
    transferdateapprove = db.Column(db.DateTime)
    remainingtotalamount = db.Column(db.Float)
    contactid = db.Column(db.String(50))
    header = db.Column(db.Boolean)
    personcardid = db.Column(db.String(20))
    namestitle = db.Column(db.String(50))
    firstname = db.Column(db.String(100))
    lastname = db.Column(db.String(100))
    fullname = db.Column(db.String(255))
    nationality = db.Column(db.String(50))
    mobile = db.Column(db.String(100))
    email = db.Column(db.String(255))

    tf01_appv_flag = db.Column(db.String(2))
    tf01_appv_date = db.Column(db.DateTime)
    tf01_appv_by = db.Column(db.String(50))
    tf01_remarks = db.Column(db.String(4000))

    tf02_appv_flag = db.Column(db.String(2))
    tf02_appv_date = db.Column(db.DateTime)
    tf02_appv_by = db.Column(db.String(50))
    tf02_remarks = db.Column(db.String(4000))

    ac01_appv_flag = db.Column(db.String(2))
    ac01_appv_date = db.Column(db.DateTime)
    ac01_appv_by = db.Column(db.String(50))
    ac01_remarks = db.Column(db.String(4000))

    ac02_appv_flag = db.Column(db.String(2))
    ac02_appv_date = db.Column(db.DateTime)
    ac02_appv_by = db.Column(db.String(50))
    ac02_remarks = db.Column(db.String(4000))

    email_sent_status = db.Column(db.String(2))
    email_sent_date = db.Column(db.DateTime)
    sms_sent_status = db.Column(db.String(2))
    sms_sent_date = db.Column(db.DateTime)
    doc_sent_status = db.Column(db.String(2))
    doc_sent_date = db.Column(db.DateTime)

    tran_status = db.Column(db.String(2))
    createby = db.Column(db.String(50))
    createdate = db.Column(db.DateTime)
    modifyby = db.Column(db.String(50))
    modifydate = db.Column(db.DateTime)

    @classmethod
    def find_by_id(cls, _hyrf_id: int) -> "CrmContactRefundModel":
        return cls.query.filter_by(hyrf_id=_hyrf_id).first()

    @classmethod
    def find_by_personalid(cls, _personal_id: str) -> List["CrmContactRefundModel"]:
        return cls.query.filter_by(personcardid=_personal_id).all()

    # @classmethod
    # def find_by_personalid(cls, _personal_id: str) -> "CrmContactRefundModel":
    #     return cls.query.filter_by(personcardid=_personal_id).first()

    @classmethod
    def find_by_contract(cls, _contract_id: str) -> List["CrmContactRefundModel"]:
        return cls.query.filter_by(contractnumber=_contract_id).all()

    @classmethod
    def find_all(cls) -> List["CrmContactRefundModel"]:
        return cls.query.all()

    @classmethod
    def find_all_tf01_appv(cls) -> List["CrmContactRefundModel"]:
        return cls.query.filter_by(tf01_appv_flag='A').all()

    @classmethod
    def find_all_tf02_appv(cls) -> List["CrmContactRefundModel"]:
        return cls.query.filter_by(tf02_appv_flag='A').all()

    @classmethod
    def find_all_ac01_appv(cls) -> List["CrmContactRefundModel"]:
        return cls.query.filter_by(ac01_appv_flag='A').all()

    @classmethod
    def find_all_ac02_appv(cls) -> List["CrmContactRefundModel"]:
        return cls.query.filter_by(ac02_appv_flag='A').all()

    def save_to_db(self) -> None:
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self) -> None:
        db.session.delete(self)
        db.session.commit()
