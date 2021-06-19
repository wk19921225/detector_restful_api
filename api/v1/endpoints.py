from system.logger import Logger
from system import variables

from flask import request
from flask_restplus import Resource

from api.restplus import api
from api.response import Response

from api.v1 import serializers

ns = api.namespace(variables.V1_NAMESPACE,
                   description=f"API Version {variables.V1_VERSION}")


def request_parse(req_data):
    # '''解析请求数据并以json形式返回'''
    data = {}
    if req_data.method == 'POST':
        data = req_data.json
    elif req_data.method == 'GET':
        data = req_data.args
    return data


# @ns.route("/")
# class Index(Resource):
#     def get(self):
#         return Response.success({
#             "description": f"{variables.SERVICE_LABEL} API "
#                            f"{variables.V1_NAMESPACE}",
#             "status": "online",
#             "version": variables.V1_VERSION
#         })


# @ns.route("/auth/register/")
# class Index(Resource):
#     @api.expect(serializers.register, validate=True)
#     def post(self):
#         body = request.json
#
#         Logger.info("A user as been registered (%s, %s).",
#                     body["username"], body["email"])
#
#         return Response.success(body, status=201)


@ns.route("/preloading")
class Preloading(Resource):
    @api.expect(serializers.preloading)
    @api.response(code=200, model=serializers.preloading_res, description="预下载识别图片")
    def get(self):
        data = request_parse(request)
        page_id = data["page_id"]
        images = data["images"]

        return Response.success({
            "page_id": page_id,
            "images": images,
        })


@ns.route("/detector")
class Detector(Resource):
    @api.expect(serializers.detector)
    @api.response(code=200, model=serializers.detector_res, description="特征识别")
    def post(self):
        data = request_parse(request)
        detector_img = data["detector_img"]
        page_id = data["detector_img"]
        target_image = data["detector_img"]
        return Response.success({
            "area": [
                {
                    "x": 0,
                    "y": 0,
                    "width": 0,
                    "height": 0,
                    "center": {
                        "x": 0,
                        "y": 0
                    }
                }
            ]
        })