from flask_restplus import fields
from api.restplus import api

# 预加载图片
preloading = api.model("Preloading", {
    "page_id": fields.String(required=True, description="当前页面ID."),
    "images": fields.String(required=True, description="当前页面ID关联的设计稿链接，使用 , 隔开."),
})

# 预加载图片响应
preloading_res = api.model("Preloading_res", {

})

point = api.model("Point", {
    "x": fields.Integer(required=True, description="横坐标"),
    "y": fields.Integer(required=True, description="纵坐标"),
})

area = api.model("Area", {
    "x": fields.Integer(required=True, description="横坐标"),
    "y": fields.Integer(required=True, description="纵坐标"),
    "width": fields.Integer(required=True, description="宽"),
    "height": fields.Integer(required=True, description="高"),
    "center": fields.Nested(required=False, model=point, description="重心"),
})
# 识别
detector = api.model("Detector", {
    "detector_img": fields.String(required=True, description="please add detectorImg."),
    "page_id": fields.String(required=True, description="please add pageId."),
    "target_image": fields.String(required=True, description="please add pageId."),
})

# 识别响应
detector_res = api.model("Detector_res", {
    "area": fields.Nested(area, as_list=True),
})
