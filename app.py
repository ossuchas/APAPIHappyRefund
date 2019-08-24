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
from resources.image import ImageUpload, Image, AvatarUpload, Avatar
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


@app.route("/")
def hello_world():
    return "Hello World! v.1.1.0"


if __name__ == "__main__":
    db.init_app(app)
    ma.init_app(app)
    app.run(host="0.0.0.0", port=5000, debug=True)
