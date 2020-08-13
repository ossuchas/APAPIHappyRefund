from db import db
from typing import List
from datetime import datetime


class CrmRefundDocrefModel(db.Model):
    __tablename__ = "crm_refund_docref"
    __table_args__ = {"schema": "RFN"}

    img_id = db.Column(db.Integer, primary_key=True)
    img_ref_contact_refund = db.Column(db.Integer)
    img_seqn = db.Column(db.Integer, default=1)
    img_type = db.Column(db.String(100))
    img_name = db.Column(db.String(255))
    # img_file = db.Column(db.VARBINARY(max))
    minio_bucket_name = db.Column(db.String(255))
    minio_img_file_name = db.Column(db.String(255))
    minio_img_url = db.Column(db.String(4000))
    createby = db.Column(db.String(50), default='flask_api')
    createdate = db.Column(db.DateTime, default=datetime.now)
    modifyby = db.Column(db.String(50), default='flask_api')
    modifydate = db.Column(db.DateTime, default=datetime.now)

    @classmethod
    def find_by_id(cls, _img_id: int) -> "CrmRefundDocrefModel":
        return cls.query.filter_by(img_id=_img_id).first()

    def save_to_db(self) -> None:
        db.session.add(self)
        db.session.commit()

        # Update Status Document to Process
        sql_statement = """
        EXECUTE [dbo].[sp_crm_procrefund_docref] @img_ref_contact_refund = {}
        """.format(self.img_ref_contact_refund)
        db.session.execute(sql_statement)
        db.session.commit()

    def exec_to_db(self) -> None:
        sql_statement = """
        EXECUTE [dbo].[sp_crm_procrefund_docref] @img_ref_contact_refund = {}
        """.format(self.img_ref_contact_refund)
        db.session.execute(sql_statement)
        db.session.commit()

    def delete_from_db(self) -> None:
        db.session.delete(self)
        db.session.commit()
