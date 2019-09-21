from db import db


class CrmRefundRoleViewModel(db.Model):
    __tablename__ = "vw_crm_refund_role"

    username = db.Column(db.String(50), primary_key=True)
    fullname = db.Column(db.String(251))
    positionname = db.Column(db.String(500))
    rolecode = db.Column(db.String(50))
    rolename = db.Column(db.String(100))
    menurefundtf1 = db.Column(db.String(2))
    menurefundtf2 = db.Column(db.String(2))
    menurefundac01 = db.Column(db.String(2))
    menurefundac02 = db.Column(db.String(2))

    @classmethod
    def check_role_tf01(cls, _user_name: str) -> "CrmRefundRoleViewModel":
        return cls.query.filter_by(menurefundtf1='1', username=_user_name).first()
