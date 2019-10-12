from ma import ma
from models.crm_param import CrmParameterModel


class CrmParameterSchema(ma.ModelSchema):
    class Meta:
        model = CrmParameterModel
