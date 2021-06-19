from flask import request
from flask_restplus import Resource

from api.response import Response
from api.restplus import api
from api.v1 import serializers
from system import variables
from system.files_operation import mkdir, cleandir, download
from system.image_detector import object_detect

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
    def post(self):
        data = request_parse(request)
        page_id = str(data["page_id"])
        images = data["images"]
        # 创建文件夹状态 boolean
        ds = mkdir(page_id)
        image_list = images.split(',')

        if not ds:
            # 创建失败 已存在 清空文件夹重新下载
            cleandir(page_id)
        image_len = len(image_list)
        for i in range(0, image_len):
            download(image_list[i], page_id)

        return Response.success({
            "page_id": page_id,
            "images": image_list,
        })


@ns.route("/detector")
class Detector(Resource):
    @api.expect(serializers.detector)
    @api.response(code=200, model=serializers.detector_res, description="特征识别")
    def post(self):
        data = request_parse(request)
        detector_image_url = data["detector_image_url"]
        page_id = str(data["page_id"])
        target_image = data["target_image"]
        object_detect(target_image, page_id, detector_image_url)
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
