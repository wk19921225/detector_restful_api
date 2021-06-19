import base64
import cv2
import numpy as np
import re
from matplotlib import pyplot as plt
from system.path import get_image_path, get_save_image_path


def decode_base64_str(img_base64_str):
    result = re.search("data:image/(?P<ext>.*?);base64,(?P<data>.*)", img_base64_str, re.DOTALL)
    if result:
        ext = result.groupdict().get("ext")
        data = result.groupdict().get("data")
        image_bin = base64.b64decode(data)
        img = np.frombuffer(image_bin, dtype=np.uint8)
        # 保留透明信息
        img_cv = cv2.imdecode(img, cv2.IMREAD_UNCHANGED)
        # cv2.imwrite(get_save_image_path(f"target.{ext}"), img_cv)
        return img
    else:
        raise Exception("Do not parse!")


def object_detect(target_base64, page_id, url):
    target_image = decode_base64_str(target_base64)
    # 用来匹配的模板图片
    template = cv2.imdecode(target_image, cv2.IMREAD_UNCHANGED)
    template_grey = cv2.cvtColor(template, cv2.COLOR_BGR2GRAY)
    # cv2.imwrite(get_save_image_path("template.png"), template_grey)
    file_path = get_image_path(page_id, url)
    # 视觉稿
    img_rgb = cv2.imread(file_path)
    img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)
    cv2.imwrite(get_save_image_path("out.png"), img_gray)
    channel, w, h = template.shape[::-1]
    # print(channel, w, h)
    res = cv2.matchTemplate(img_gray, template_grey, cv2.TM_CCOEFF_NORMED)
    threshold = 0.4
    loc = np.where(res >= threshold)
    for pt in zip(*loc[::-1]):
        cv2.rectangle(img_rgb, pt, (pt[0] + w, pt[1] + h), (0, 0, 255), 1)
    cv2.imwrite(get_save_image_path("output.png"), img_rgb)
