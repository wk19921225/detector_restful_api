import base64
import cv2
import numpy as np
import re
import time
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


MIN_MATCH_COUNT = 20  # 设置最低特征点匹配数量为10


def object_detect(target_base64, page_id, url):
    target_image = decode_base64_str(target_base64)
    # 用来匹配的模板图片
    template = cv2.imdecode(target_image, cv2.COLOR_BGR2GRAY)
    cv2.imwrite(get_save_image_path("template.png"), template)
    file_path = get_image_path(page_id, url)
    # 视觉稿
    img_relay = cv2.imread(file_path, cv2.COLOR_BGR2GRAY)

    #  计算特征点提取&生成描述时间
    # start = time.time()
    # 创建sift检测器
    sift = cv2.xfeatures2d.SIFT_create()
    # 使用SIFT查找关键点key points和描述符descriptors
    kp1, des1 = sift.detectAndCompute(template, None)
    kp2, des2 = sift.detectAndCompute(img_relay, None)
    # end = time.time()
    # print("特征点提取&生成描述运行时间:%.2f秒" % (end - start))
    #
    # kp_image1 = cv2.drawKeypoints(template, kp1, None)
    # kp_image2 = cv2.drawKeypoints(img_relay, kp2, None)
    #
    # plt.figure()
    # plt.imshow(kp_image1)
    # plt.savefig(get_save_image_path('kp_image1.png'), dpi=300)
    #
    # plt.figure()
    # plt.imshow(kp_image2)
    # plt.savefig(get_save_image_path('kp_image2.png'), dpi=300)

    # 创建设置FLANN匹配
    FLANN_INDEX_KDTREE = 0
    index_params = dict(algorithm=FLANN_INDEX_KDTREE, trees=5)
    search_params = dict(checks=100)
    flann = cv2.FlannBasedMatcher(index_params, search_params)
    matches = flann.knnMatch(des1, des2, k=2)
    # 存储匹配值
    good = []
    # 舍弃大于0.7的匹配
    for m, n in matches:
        if m.distance < 0.9 * n.distance:
            good.append(m)
    if len(good) > MIN_MATCH_COUNT:
        # 获取关键点的坐标
        src_pts = np.float32([kp1[m.queryIdx].pt for m in good]).reshape(-1, 1, 2)
        dst_pts = np.float32([kp2[m.trainIdx].pt for m in good]).reshape(-1, 1, 2)
        # 计算变换矩阵和MASK
        M, mask = cv2.findHomography(src_pts, dst_pts, cv2.RANSAC, 5.0)
        # matches_mask = mask.ravel().tolist()
        h, w, c = template.shape
        # 使用得到的变换矩阵对原图像的四个角进行变换，获得在目标图像上对应的坐标
        pts = np.float32([[0, 0], [0, h - 1], [w - 1, h - 1], [w - 1, 0]]).reshape(-1, 1, 2)
        areas = cv2.perspectiveTransform(pts, M)
        cv2.polylines(img_relay, [np.int32(areas)], True, (0, 255, 0), 2, cv2.LINE_AA)
        [[ltx, lty], [lbx, lby], [rtx, rty], [rbx, rby]] = np.squeeze(areas).tolist()
        return {
            "left_top": {"x": ltx, "y": lty},
            "left_bottom": {"x": lbx, "y": lby},
            "right_top": {"x": rtx, "y": rty},
            "right_bottom": {"x": rbx, "y": rby},
            "center": {"x": (ltx + rtx + lbx + rbx) / 4, "y": (lty + rty + lby + rby) / 4},
        }
        # for i in areas.length:
        #     # print(area.flatten())
        #     w, h = areas[i].shape
        #     print(w, h)
        #     print(type(areas))
        # cv2.imwrite(get_save_image_path("img_relay.png"), img_relay)
    else:
        print("Not enough matches are found - %d/%d" % (len(good), MIN_MATCH_COUNT))
        matches_mask = None
    # draw_params = dict(matchColor=(0, 255, 0),
    #                    singlePointColor=None,
    #                    matchesMask=matches_mask,
    #                    flags=2)
    # result = cv2.drawMatches(template, kp1, img_relay, kp2, good, None, **draw_params)
    # cv2.imwrite(get_save_image_path("result.png"), result)
    # plt.imshow(result, 'gray')
    # plt.show()
