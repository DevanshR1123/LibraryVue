from flask_restful import Resource, fields, marshal
from flask_security import auth_required

test_api_resource_fields = {
    "msg": fields.String,
}


class TestAPI(Resource):
    @auth_required("token")
    def get(self):
        return marshal({"msg": "Hello World from TestAPI"}, test_api_resource_fields)
