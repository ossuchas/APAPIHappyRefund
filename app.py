from flask import Flask, jsonify
from flask_restful import Api
from dotenv import load_dotenv
from flask_cors import CORS
from flask_uploads import configure_uploads, patch_request_class, UploadSet, IMAGES, config_for_set
from marshmallow import ValidationError

from db import db
from ma import ma

from resources.crm_contact_refund import CrmContactRefund, CrmContactRefundList, CrmContactRefundPersonalIdList, CrmCustomerRefund
from resources.userauthen import UserLogin
from resources.crm_contact_refund_tf01 import CrmContactRefundListCSSent, CrmContactRefundTF01, CrmContactRefundListTF01
from resources.crm_contact_refund_tf02 import CrmContactRefundListTF01Appv, CrmContactRefundTF02, CrmContactRefundListTF02
from resources.crm_contact_refund_ac01 import CrmContactRefundListTF02Appv, CrmContactRefundAC01, CrmContactRefundListAC01
from resources.crm_contact_refund_ac02 import CrmContactRefundListAC01Appv, CrmContactRefundAC02, CrmContactRefundListAC02, CrmContactRefundAC02Reject

from resources.vw_crm_refund_docref import CrmContactRefundListImgUrl
from resources.vw_crm_refund_appv4 import CrmContactRefundAppv4View
from resources.image import ImageUpload, Image, AvatarUpload, Avatar

from resources.vw_crm_refund_role import CrmRefundRoleAuth

from libs.image_helper import IMAGE_SET

app = Flask(__name__)
CORS(app, resources=r"/api/*", allow_headers="Content-Type")

load_dotenv(".env", verbose=True)
app.config.from_object("config")
app.config.from_envvar("APPLICATION_SETTING")


configure_uploads(app, IMAGE_SET)
patch_request_class(app, 10 * 1024 * 1024)  # restrict max upload image size to 10MB

api = Api(app, prefix="/api/v1")


@app.before_first_request
def create_tables():
    db.create_all()


@app.errorhandler(ValidationError)
def handle_marshmallow_validation(err):
    return jsonify(err.messages), 400


api.add_resource(CrmContactRefundList, "/refundlist")
api.add_resource(CrmContactRefund, "/refund/<int:hyrf_id>")
api.add_resource(UserLogin, "/login")

api.add_resource(ImageUpload, "/upload/image")
api.add_resource(Image, "/image/<string:filename>")
api.add_resource(AvatarUpload, "/upload/avatar")
api.add_resource(Avatar, "/avatar/<int:user_id>")

# for Customer
api.add_resource(CrmContactRefundPersonalIdList, "/checkpersonalid/<string:personal_id>")
api.add_resource(CrmCustomerRefund, "/senddoc/<int:hyrf_id>")

# For TF01
api.add_resource(CrmContactRefundListCSSent, "/cssentlist")
api.add_resource(CrmContactRefundListTF01, "/tf01alllist")
api.add_resource(CrmContactRefundTF01, "/tf01approved/<int:hyrf_id>")

# For TF02
api.add_resource(CrmContactRefundListTF01Appv, "/tf01appvlist")
api.add_resource(CrmContactRefundListTF02, "/tf02alllist")
api.add_resource(CrmContactRefundTF02, "/tf02approved/<int:hyrf_id>")

# For AC01
api.add_resource(CrmContactRefundListTF02Appv, "/tf02appvlist")
api.add_resource(CrmContactRefundListAC01, "/ac01alllist")
api.add_resource(CrmContactRefundAC01, "/ac01approved/<int:hyrf_id>")

# For AC02
api.add_resource(CrmContactRefundListAC01Appv, "/ac01appvlist")
api.add_resource(CrmContactRefundListAC02, "/ac02alllist")
api.add_resource(CrmContactRefundAC02, "/ac02approved/<int:hyrf_id>")
api.add_resource(CrmContactRefundAC02Reject, "/ac02reject/<int:hyrf_id>")

# List Image Url
api.add_resource(CrmContactRefundListImgUrl, "/imageurls/<int:hyrf_id>")

# List Unit Appoved 4
api.add_resource(CrmContactRefundAppv4View, "/appv4list")

# Check Role Page
api.add_resource(CrmRefundRoleAuth, "/checkroleauth/<string:user_name>")


@app.route("/")
def hello_world():
    return "Happy Refund v.1.0.0"


if __name__ == "__main__":
    db.init_app(app)
    ma.init_app(app)
    app.run(host="0.0.0.0", port=5000, debug=True)
