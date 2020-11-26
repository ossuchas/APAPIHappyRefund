from db import db
from typing import List
from sqlalchemy.dialects.postgresql import UUID
from uuid import uuid4


class CrmContactRefundModel(db.Model):
    __tablename__ = "crm_contact_refund"
    __table_args__ = {"schema": "RFN"}

    hyrf_id = db.Column(db.Integer, primary_key=True)
    productid = db.Column(db.String(15))
    project = db.Column(db.String(255))
    companyid = db.Column(db.String(15))
    unitnumber = db.Column(db.String(10))
    wbsnumber = db.Column(db.String(30))
    contractnumber = db.Column(db.String(20))
    transfernumber = db.Column(db.String(50))
    transferdateapprove = db.Column(db.DateTime)
    remainingtotalamount = db.Column(db.Float)
    contactid = db.Column(db.String(50))
    header = db.Column(db.Boolean)
    personcardid = db.Column(db.String(20))
    namestitle = db.Column(db.String(50))
    firstname = db.Column(db.String(100))
    lastname = db.Column(db.String(100))
    fullname = db.Column(db.String(255))
    coownername = db.Column(db.String(500))
    nationality = db.Column(db.String(50))
    foreigner = db.Column(db.String(2))
    mobile = db.Column(db.String(100))
    email = db.Column(db.String(255))

    bankcode = db.Column(db.String(15))
    bankaccountno = db.Column(db.String(20))
    bankaccountname = db.Column(db.String(500))
    legalentityid = db.Column(db.String(10))
    legalentiryname = db.Column(db.String(1000))
    legalbankcode = db.Column(db.String(15))
    legalbankaccountno = db.Column(db.String(20))

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
    ac02_due_date = db.Column(db.DateTime)

    ac03_reject_doc_flag = db.Column(db.String(2))
    ac03_reject_reason = db.Column(db.String(500))
    ac03_change_due_flag = db.Column(db.String(2))
    ac03_change_due_date = db.Column(db.DateTime)

    email_sent_status = db.Column(db.String(2))
    email_sent_date = db.Column(db.DateTime)
    email_thx_sent_status = db.Column(db.String(2))
    email_thx_sent_date = db.Column(db.DateTime)

    email_reject_doc_status = db.Column(db.String(2))
    email_reject_doc_date = db.Column(db.DateTime)
    email_change_due = db.Column(db.String(2))
    email_change_due_date = db.Column(db.DateTime)

    sms_sent_status = db.Column(db.String(2))
    sms_sent_date = db.Column(db.DateTime)
    sms_thx_sent_status = db.Column(db.String(2))
    sms_thx_sent_date = db.Column(db.DateTime)

    sms_reject_doc_status = db.Column(db.String(2))
    sms_reject_doc_date = db.Column(db.DateTime)
    sms_change_due = db.Column(db.String(2))
    sms_change_due_date = db.Column(db.DateTime)

    line_sent_status = db.Column(db.String(2))
    line_sent_date = db.Column(db.DateTime)

    doc_sent_status = db.Column(db.String(2))
    doc_sent_date = db.Column(db.DateTime)
    doc_merge_url = db.Column(db.String(255))

    tran_status = db.Column(db.String(2))
    createby = db.Column(db.String(50))
    createdate = db.Column(db.DateTime)
    modifyby = db.Column(db.String(50))
    modifydate = db.Column(db.DateTime)

    # modified by Suchat S. 2020-10-20 for add new transfer id
    transferid = db.Column(UUID(as_uuid=True), nullable=True)

    @classmethod
    def find_by_id(cls, _hyrf_id: int) -> "CrmContactRefundModel":
        return cls.query.filter_by(hyrf_id=_hyrf_id).first()

    # @classmethod
    # def find_by_personalid(cls, _personal_id: str) -> List["CrmContactRefundModel"]:
    #     return cls.query.filter_by(personcardid=_personal_id).all()

    @classmethod
    def find_by_personalid(cls, _personal_id: str) -> "CrmContactRefundModel":
        return cls.query.filter_by(personcardid=_personal_id).first()

    @classmethod
    def find_by_personalidlist(cls, _personal_id: str) -> List["CrmContactRefundModel"]:
        # return cls.query.filter_by(personcardid=_personal_id).all()
        return cls.query.filter_by(personcardid=_personal_id, ).order_by(cls.doc_sent_status.desc(), cls.modifydate.asc(), cls.doc_sent_date.asc()).all()

    @classmethod
    def find_by_contract(cls, _contract_id: str) -> List["CrmContactRefundModel"]:
        return cls.query.filter_by(contractnumber=_contract_id).all()

    @classmethod
    def find_all(cls) -> List["CrmContactRefundModel"]:
        return cls.query.all()

    # for Customer
    @classmethod
    def find_all_cs_sent(cls) -> List["CrmContactRefundModel"]:
        return cls.query.filter(
            (cls.tf01_appv_flag == 'N') | (cls.tf01_appv_flag == 'R') |
            (cls.tf02_appv_flag == 'R') | (cls.ac01_appv_flag == 'R') | (cls.ac02_appv_flag == 'R'),
            (cls.doc_sent_status == 'Y') | (cls.doc_sent_status == 'P') | (cls.doc_sent_status == 'R'),
            (cls.tran_status == 'A')
        ).order_by(cls.modifydate.desc()).all()

    @classmethod
    def find_txt_search_cs_sent(cls, str_search: str) -> List["CrmContactRefundModel"]:
        return cls.query.filter(
            (cls.tf01_appv_flag == 'N') | (cls.tf01_appv_flag == 'R') |
            (cls.tf02_appv_flag == 'R') | (cls.ac01_appv_flag == 'R') | (cls.ac02_appv_flag == 'R'),
            (cls.doc_sent_status == 'Y') | (cls.doc_sent_status == 'P') | (cls.doc_sent_status == 'R'),
            (cls.tran_status == 'A'),
            (cls.unitnumber.like('%' + str_search + '%')) |
            (cls.productid.like('%' + str_search + '%')) |
            (cls.project.like('%' + str_search + '%')) |
            (cls.fullname.like('%' + str_search + '%')) |
            (cls.coownername.like('%' + str_search + '%'))
        ).order_by(cls.modifydate.desc()).all()

    @classmethod
    def validate_id_sent(cls, _contract_id: str) -> List["CrmContactRefundModel"]:
        return cls.query.filter_by(contractnumber=_contract_id, doc_sent_status='Y').all()

    @classmethod
    def find_all_tf01_appv(cls) -> List["CrmContactRefundModel"]:
        return cls.query.filter_by(tf01_appv_flag='A', tran_status='A').order_by(cls.modifydate.desc()).all()

    @classmethod
    def find_txt_search_tf01_appv(cls, str_search: str) -> List["CrmContactRefundModel"]:
        return cls.query.filter(
            (cls.tf01_appv_flag == 'A'), (cls.tran_status == 'A'),
            (cls.unitnumber.like('%' + str_search + '%')) |
            (cls.productid.like('%' + str_search + '%')) |
            (cls.project.like('%' + str_search + '%')) |
            (cls.fullname.like('%' + str_search + '%')) |
            (cls.coownername.like('%' + str_search + '%'))
        ).order_by(cls.modifydate.desc()).all()

    @classmethod
    def find_all_tf01_rejt(cls) -> List["CrmContactRefundModel"]:
        return cls.query.filter_by(tf01_appv_flag='R', tran_status='A').order_by(cls.modifydate.desc()).all()

    @classmethod
    def find_all_tf01_all(cls) -> List["CrmContactRefundModel"]:
        return cls.query.filter(
            (cls.tf02_appv_flag == 'N'),
            (cls.tf01_appv_flag == 'A'), (cls.tran_status == 'A')).order_by(cls.modifydate.desc()).all()

    @classmethod
    def find_all_tf02_appv(cls) -> List["CrmContactRefundModel"]:
        return cls.query.filter_by(tf02_appv_flag='A', tran_status='A').order_by(cls.modifydate.desc()).all()

    @classmethod
    def find_txt_search_tf02_appv(cls, str_search: str) -> List["CrmContactRefundModel"]:
        return cls.query.filter(
            (cls.tf02_appv_flag == 'A'), (cls.tran_status == 'A'),
            (cls.unitnumber.like('%' + str_search + '%')) |
            (cls.productid.like('%' + str_search + '%')) |
            (cls.project.like('%' + str_search + '%')) |
            (cls.fullname.like('%' + str_search + '%')) |
            (cls.coownername.like('%' + str_search + '%'))
        ).order_by(cls.modifydate.desc()).all()

    @classmethod
    def find_all_tf02_rejt(cls) -> List["CrmContactRefundModel"]:
        return cls.query.filter_by(tf02_appv_flag='R', tran_status='A').order_by(cls.modifydate.desc()).all()

    @classmethod
    def find_all_tf02_all(cls) -> List["CrmContactRefundModel"]:
        return cls.query.filter(
            (cls.ac01_appv_flag == 'N'),
            (cls.tf02_appv_flag == 'A'), (cls.tran_status == 'A')).order_by(cls.modifydate.desc()).all()

    @classmethod
    def find_all_ac01_appv(cls) -> List["CrmContactRefundModel"]:
        return cls.query.filter_by(ac01_appv_flag='A', tran_status='A').order_by(cls.modifydate.desc()).all()

    @classmethod
    def find_txt_search_ac01_appv(cls, str_search: str) -> List["CrmContactRefundModel"]:
        return cls.query.filter(
            (cls.ac01_appv_flag == 'A'), (cls.tran_status == 'A'),
            (cls.unitnumber.like('%' + str_search + '%')) |
            (cls.productid.like('%' + str_search + '%')) |
            (cls.project.like('%' + str_search + '%')) |
            (cls.fullname.like('%' + str_search + '%')) |
            (cls.coownername.like('%' + str_search + '%'))
        ).order_by(cls.modifydate.desc()).all()

    @classmethod
    def find_all_ac01_rejt(cls) -> List["CrmContactRefundModel"]:
        return cls.query.filter_by(ac01_appv_flag='R', tran_status='A').order_by(cls.modifydate.desc()).all()

    @classmethod
    def find_all_ac01_all(cls) -> List["CrmContactRefundModel"]:
        # return cls.query.filter((cls.ac02_appv_flag == 'N') |
        #                         (cls.ac02_appv_flag == 'R'),
        #                         (cls.ac01_appv_flag == 'A')).order_by(cls.modifydate.desc()).all()
        return cls.query.filter(
            (cls.ac02_appv_flag == 'N'),
            (cls.ac01_appv_flag == 'A'), (cls.tran_status == 'A')).order_by(cls.modifydate.desc()).all()

    @classmethod
    def find_all_ac02_appv(cls) -> List["CrmContactRefundModel"]:
        # return cls.query.filter_by(ac02_appv_flag='A').order_by(cls.modifydate.desc()).all()
        return cls.query.filter(
            (cls.ac02_appv_flag == 'A'),
            (cls.createdate >= '2019-09-26 00:00:00.001'), (cls.tran_status == 'A')).order_by(cls.modifydate.desc()).all()

    @classmethod
    def find_all_ac02_rejt(cls) -> List["CrmContactRefundModel"]:
        return cls.query.filter_by(ac02_appv_flag='R', tran_status='A').order_by(cls.modifydate.desc()).all()

    @classmethod
    def find_all_ac02_all(cls) -> List["CrmContactRefundModel"]:
        return cls.query.filter(
            (cls.ac02_appv_flag == 'A') |
            (cls.ac02_appv_flag == 'R'), (cls.tran_status == 'A')
        ).order_by(cls.modifydate.desc()).all()

    def save_to_db(self) -> None:
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self) -> None:
        db.session.delete(self)
        db.session.commit()
