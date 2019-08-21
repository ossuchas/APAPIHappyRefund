from db import db
from typing import List


class CrmRefundDocrefModel(db.Model):
    __tablename__ = "crm_refund_docref"

    img_id = db.Column(db.Integer, primary_key=True)
    img_ref_contact_refund = db.Column(db.Integer)
    img_seqn = db.Column(db.Integer)
    img_type = db.Column(db.String(100))
    img_name = db.Column(db.String(255))
    img_file = db.Column(db.VARBINARY(max))
    createby = db.Column(db.String(50))
    createdate = db.Column(db.DateTime)
    modifyby = db.Column(db.String(50))
    modifydate = db.Column(db.DateTime)

    @classmethod
    def find_by_id(cls, _img_id: int) -> "CrmRefundDocrefModel":
        return cls.query.filter_by(img_id=_img_id).first()

    def save_to_db(self) -> None:
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self) -> None:
        db.session.delete(self)
        db.session.commit()
