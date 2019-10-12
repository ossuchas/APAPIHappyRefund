from db import db
from typing import List
from datetime import datetime


class CrmParameterModel(db.Model):
    __tablename__ = "crm_param"

    param_id = db.Column(db.Integer, primary_key=True)
    param_code = db.Column(db.String(50))
    param_seqn = db.Column(db.Integer)
    param_vlue = db.Column(db.String(4000))
    param_data = db.Column(db.String(250))
    long_desc = db.Column(db.String(255))
    remarks = db.Column(db.String(4000))
    createby = db.Column(db.String(50), default='suchat_s')
    createdate = db.Column(db.DateTime, default=datetime.now)
    modifyby = db.Column(db.String(50), default='suchat_s')
    modifydate = db.Column(db.DateTime, default=datetime.now)

    @classmethod
    def find_by_id(cls, _param_id: int) -> "CrmParameterModel":
        return cls.query.filter_by(param_id=_param_id).first()

    @classmethod
    def find_by_code(cls) -> List["CrmParameterModel"]:
        return cls.query.filter_by(param_code='CRM_CANCELAC03_REFUND').order_by(cls.param_seqn).all()

    def save_to_db(self) -> None:
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self) -> None:
        db.session.delete(self)
        db.session.commit()
