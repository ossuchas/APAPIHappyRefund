from flask import Flask
from flask_restful import Api
from dotenv import load_dotenv
from flask_cors import CORS

from db import db
from ma import ma

from resources.crm_contact_refund import CrmContactRefund, CrmContactRefundList
from resources.userauthen import UserLogin

app = Flask(__name__)
CORS(app, resources=r"/api/*", allow_headers="Content-Type")

load_dotenv(".env", verbose=True)
app.config.from_object("config")
app.config.from_envvar("APPLICATION_SETTING")

api = Api(app, prefix="/api/v1")


@app.before_first_request
def create_tables():
    db.create_all()


api.add_resource(CrmContactRefundList, "/refundlist")
api.add_resource(CrmContactRefund, "/refund/<int:hyrf_id>")
api.add_resource(UserLogin, "/login")


@app.route("/")
def hello_world():
    return "Hello World!"


if __name__ == "__main__":
    db.init_app(app)
    ma.init_app(app)
    app.run(host="0.0.0.0", port=5000, debug=True)
