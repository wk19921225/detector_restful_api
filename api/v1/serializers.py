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
    "x": fields.Float(required=True, description="横坐标"),
    "y": fields.Float(required=True, description="纵坐标"),
})

area = api.model("Area", {
    "left_top": fields.Nested(point, description="左上位置坐标"),
    "left_bottom": fields.Nested(point, description="左下位置坐标"),
    "right_top": fields.Nested(point, description="右上位置坐标"),
    "right_bottom": fields.Nested(point, description="右下位置坐标"),
    "center": fields.Nested(point, description="重心"),
})
# 识别
detector = api.model("Detector", {
    "detector_image_url": fields.String(required=True, description="指定需要匹配的设计稿图片."),
    "page_id": fields.String(required=True, description="当前页面id."),
    "target_image": fields.String(required=True, description="目标元素的base64编码图."),
})

# 识别响应
detector_res = api.model("Detector_res", {
    "area": fields.Nested(area, as_list=True),
})
