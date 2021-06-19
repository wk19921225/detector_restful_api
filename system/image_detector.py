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


MIN_MATCH_COUNT = 10  # 设置最低特征点匹配数量为10


def object_detect(target_base64, page_id, url):
    target_image = decode_base64_str(target_base64)
    # 用来匹配的模板图片
    template = cv2.imdecode(target_image, cv2.COLOR_BGR2BGRA)
    # cv2.imwrite(get_save_image_path("template.png"), template_grey)
    file_path = get_image_path(page_id, url)
    # 视觉稿
    img_relay = cv2.imread(file_path, cv2.COLOR_BGR2BGRA)

    # Initiate SIFT detector创建sift检测器
    sift = cv2.xfeatures2d.SIFT_create()
    # find the keypoints and descriptors with SIFT
    kp1, des1 = sift.detectAndCompute(template, None)
    kp2, des2 = sift.detectAndCompute(img_relay, None)

    # 创建设置FLANN匹配
    FLANN_INDEX_KDTREE = 0
    index_params = dict(algorithm=FLANN_INDEX_KDTREE, trees=5)
    search_params = dict(checks=50)
    flann = cv2.FlannBasedMatcher(index_params, search_params)
    matches = flann.knnMatch(des1, des2, k=2)
    # store all the good matches as per Lowe's ratio test.
    good = []
    # 舍弃大于0.7的匹配
    for m, n in matches:
        if m.distance < 0.7 * n.distance:
            good.append(m)
    if len(good) > MIN_MATCH_COUNT:
        # 获取关键点的坐标
        src_pts = np.float32([kp1[m.queryIdx].pt for m in good]).reshape(-1, 1, 2)
        dst_pts = np.float32([kp2[m.trainIdx].pt for m in good]).reshape(-1, 1, 2)
        # 计算变换矩阵和MASK
        M, mask = cv2.findHomography(src_pts, dst_pts, cv2.RANSAC, 5.0)
        matchesMask = mask.ravel().tolist()
        h, w = template.shape
        # 使用得到的变换矩阵对原图像的四个角进行变换，获得在目标图像上对应的坐标
        pts = np.float32([[0, 0], [0, h - 1], [w - 1, h - 1], [w - 1, 0]]).reshape(-1, 1, 2)
        dst = cv2.perspectiveTransform(pts, M)
        cv2.polylines(img_relay, [np.int32(dst)], True, 0, 2, cv2.LINE_AA)
    else:
        print("Not enough matches are found - %d/%d" % (len(good), MIN_MATCH_COUNT))
        matchesMask = None
    draw_params = dict(matchColor=(0, 255, 0),
                       singlePointColor=None,
                       matchesMask=matchesMask,
                       flags=2)
    result = cv2.drawMatches(template, kp1, img_relay, kp2, good, None, **draw_params)
    plt.imshow(result, 'gray')
    plt.show()
