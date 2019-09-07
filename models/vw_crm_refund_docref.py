from db import db
from typing import List


class CrmRefundDocrefViewModel(db.Model):
    __tablename__ = "vw_crm_refund_docref"

    img_id = db.Column(db.Integer, primary_key=True)
    img_ref_contact_refund = db.Column(db.Integer)
    img_seqn = db.Column(db.Integer, default=1)
    img_name = db.Column(db.String(255))
    img_url = db.Column(db.String(400))

    @classmethod
    def find_by_id(cls, _hyrf_id: int) -> List["CrmRefundDocrefViewModel"]:
        return cls.query.filter_by(img_ref_contact_refund=_hyrf_id).all()
